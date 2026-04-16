import csv
import os
import uuid
from decimal import Decimal
from datetime import datetime

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import transaction, connection, IntegrityError

from api_telemetria.models import (
    MedicaoVeiculoTemp,
    Veiculo,
    Medicao,
    MedicaoVeiculoIoT,
)
import logging

logger = logging.getLogger(__name__)


def executar_procedure_pos_importacao(arquivoid):
    with connection.cursor() as cursor:
        cursor.callproc("processa_arquivo", [arquivoid])


def processar_csv_medicoes(arquivo):
    arquivoid = str(uuid.uuid4())

    pasta_destino = os.path.join(settings.MEDIA_ROOT, "importacoes_medicao")
    os.makedirs(pasta_destino, exist_ok=True)

    nome_salvo = f"{arquivoid}_{arquivo.name}"
    fs = FileSystemStorage(location=pasta_destino)
    nome_arquivo_salvo = fs.save(nome_salvo, arquivo)
    caminho_completo = os.path.join(pasta_destino, nome_arquivo_salvo)

    total_linhas_arquivo = 0
    erros = []
    linhas_para_inserir = []

    veiculos_cache = {v.id: v for v in Veiculo.objects.all()}  # type: ignore
    medicoes_cache = {m.id: m for m in Medicao.objects.all()}  # type: ignore

    with open(caminho_completo, mode="r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")

        campos_esperados = {"veiculoid", "medicaoid", "data", "valor"}

        if not reader.fieldnames:
            raise ValueError("O CSV não possui cabeçalho.")

        if not campos_esperados.issubset(set(reader.fieldnames)):
            raise ValueError(
                f"Cabeçalho inválido. Esperado: {list(campos_esperados)}. Recebido: {reader.fieldnames}"
            )

        for numero_linha, row in enumerate(reader, start=2):
            total_linhas_arquivo += 1

            try:
                id_veiculo = int(row["veiculoid"])
                id_medicao = int(row["medicaoid"])

                veiculo = veiculos_cache.get(id_veiculo)
                if not veiculo:
                    raise LookupError(f"Veículo {id_veiculo} não encontrado.")

                medicao = medicoes_cache.get(id_medicao)
                if not medicao:
                    raise LookupError(f"Medição {id_medicao} não encontrada.")

                data_convertida = datetime.strptime(
                    row["data"].strip(), "%Y-%m-%d %H:%M:%S"
                )

                valor_convertido = Decimal(row["valor"].strip())

                linhas_para_inserir.append(
                    MedicaoVeiculoTemp(
                        veiculoid=veiculo,
                        medicaoid=medicao,
                        data=data_convertida,
                        valor=valor_convertido,
                        arquivoid=arquivoid,
                    )
                )

            except Exception as e:
                erros.append({"linha": numero_linha, "erro": str(e)})

    total_linhas_validas = len(linhas_para_inserir)

    with transaction.atomic():
        if linhas_para_inserir:
            MedicaoVeiculoTemp.objects.bulk_create(linhas_para_inserir, batch_size=1000)

        total_linhas_importadas = MedicaoVeiculoTemp.objects.filter(
            arquivoid=arquivoid
        ).count()

        quantidades_conferem = total_linhas_validas == total_linhas_importadas

        if quantidades_conferem:
            executar_procedure_pos_importacao(arquivoid)
        else:
            MedicaoVeiculoTemp.objects.filter(arquivoid=arquivoid).delete()

    return {
        "arquivoid": arquivoid,
        "arquivo_salvo": nome_arquivo_salvo,
        "caminho": caminho_completo,
        "total_linhas_arquivo": total_linhas_arquivo,
        "total_linhas_importadas": total_linhas_importadas,
        "quantidades_conferem": total_linhas_arquivo == total_linhas_importadas,
        "erros": erros,
    }


class SyncService:
    """
    Service layer pura. Isola as regras de negócio de IoT.
    Trata sincronização offline do ESP32 com zero tolerância a corrupção de dados.
    """

    @staticmethod
    def processar_sync_offline(veiculo_id: int, medicoes_data: list) -> dict:
        """
        Pega a porrada de dados do ESP32 que ficou offline e joga no banco de uma vez.
        Usa transação atômica e bulk_create pra não fritar o DB.

        Args:
            veiculo_id: ID do veículo que está sincronizando
            medicoes_data: Lista de dicts com chaves: temperatura, vibracao, rpm, timestamp_coleta

        Returns:
            Dict com status, registros inseridos e detalhes de erro (se houver)

        Raises:
            ValueError: Se veículo não existe (race condition: deletado entre validação e insert)
            IntegrityError: Se houver violação de constraint no banco
        """
        if not medicoes_data:
            return {
                "status": "ignorado",
                "msg": "Sem dados novos para sincronizar.",
                "registros_inseridos": 0,
            }

        novas_medicoes = []
        registros_processados = 0

        try:
            with transaction.atomic():
                # Validação atômica: garante que veículo não foi deletado entre validação e insert
                veiculo = Veiculo.objects.select_for_update().get(id=veiculo_id)

                for item in medicoes_data:
                    registros_processados += 1
                    try:
                        novas_medicoes.append(
                            MedicaoVeiculoIoT(
                                veiculo=veiculo,
                                temperatura=item["temperatura"],
                                vibracao=item["vibracao"],
                                rpm=item["rpm"],
                                timestamp_coleta=item["timestamp_coleta"],
                            )
                        )
                    except (ValueError, TypeError, KeyError) as e:
                        # Se um item for malformado, loga e pula pra próximo
                        logger.warning(
                            f"Registro malformado do veículo {veiculo_id} (idx {registros_processados}): {str(e)}. Pulando."
                        )
                        continue

                if not novas_medicoes:
                    return {
                        "status": "erro",
                        "msg": "Nenhum registro válido após validação.",
                        "registros_inseridos": 0,
                    }

                # bulk_create com ignore_conflicts resolve duplicatas de retransmissão
                resultado = MedicaoVeiculoIoT.objects.bulk_create(
                    novas_medicoes, batch_size=500, ignore_conflicts=True
                )

                registros_inseridos = len(resultado)

                logger.info(
                    f"✓ Sync concluído: {registros_inseridos} registros do veículo "
                    f"{veiculo_id} ({registros_processados} processados)"
                )

                return {
                    "status": "sucesso",
                    "registros_inseridos": registros_inseridos,
                    "registros_processados": registros_processados,
                    "veiculo_id": veiculo_id,
                }

        except Veiculo.DoesNotExist:
            # Race condition: veículo foi deletado entre validação e insert
            logger.error(
                f"✗ Race condition: Veículo {veiculo_id} não existe mais. "
                f"Rollback automático."
            )
            return {
                "status": "erro",
                "msg": f"Veículo {veiculo_id} não encontrado no banco.",
                "registros_inseridos": 0,
                "código_erro": "VEICULO_NAO_EXISTE",
            }

        except IntegrityError as e:
            # Violação de constraint → rollback todo o batch
            logger.error(
                f"✗ Falha de integridade no sync do veículo {veiculo_id}: {str(e)}. "
                f"Rollback de {registros_processados} tentativas."
            )
            return {
                "status": "erro",
                "msg": "Falha de integridade no banco. Nenhum registro foi inserido (rollback automático).",
                "registros_inseridos": 0,
                "código_erro": "INTEGRITY_ERROR",
                "detalhe_tecnico": str(e)[:200],
            }

        except Exception as e:
            logger.error(
                f"✗ Falha catastrófica no sync do veículo {veiculo_id}: {str(e)}"
            )
            return {
                "status": "erro",
                "msg": "Erro desconhecido ao sincronizar.",
                "registros_inseridos": 0,
                "código_erro": "ERRO_DESCONHECIDO",
            }
