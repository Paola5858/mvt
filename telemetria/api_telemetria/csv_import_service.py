import csv
import logging
from datetime import datetime
from decimal import Decimal
from django.db import transaction
from api_telemetria.models import MedicaoVeiculo, Veiculo, Medicao

logger = logging.getLogger(__name__)

def processar_csv_para_medicoes(csv_file):
    """
    Processa um arquivo CSV para importar medições de veículos diretamente para MedicaoVeiculo.
    Realiza validações e inserção em lote.
    """
    reader = csv.DictReader(csv_file, delimiter=";")

    campos_esperados = {"veiculoid", "medicaoid", "data", "valor"}
    if not reader.fieldnames or not campos_esperados.issubset(set(reader.fieldnames)):
        raise ValueError(f"Cabeçalho CSV inválido. Esperado: {list(campos_esperados)}. Recebido: {reader.fieldnames}")

    veiculos_cache = {v.id: v for v in Veiculo.objects.all()}  # type: ignore
    medicoes_cache = {m.id: m for m in Medicao.objects.all()}  # type: ignore

    medicoes_para_criar = []
    erros = []

    for numero_linha, row in enumerate(reader, start=2):
        try:
            veiculo_id = int(row["veiculoid"])
            medicao_id = int(row["medicaoid"])
            valor = Decimal(row["valor"].strip())

            veiculo = veiculos_cache.get(veiculo_id)
            if not veiculo:
                raise ValueError(f"Veículo {veiculo_id} não encontrado na linha {numero_linha}.")

            medicao = medicoes_cache.get(medicao_id)
            if not medicao:
                raise ValueError(f"Medição {medicao_id} não encontrada na linha {numero_linha}.")

            data_convertida = datetime.strptime(row["data"].strip(), "%Y-%m-%d %H:%M:%S")

            medicoes_para_criar.append(
                MedicaoVeiculo(
                    veiculo=veiculo,
                    medicao=medicao,
                    data=data_convertida,
                    valor=valor,
                )
            )
        except Exception as e:
            erros.append({"linha": numero_linha, "erro": str(e), "dados": row})
            logger.error(f"Erro na linha {numero_linha} do CSV: {e} - Dados: {row}")

    total_linhas_processadas = numero_linha - 1 if 'numero_linha' in locals() else 0

    if medicoes_para_criar:
        with transaction.atomic():
            MedicaoVeiculo.objects.bulk_create(medicoes_para_criar, batch_size=1000)
            logger.info(f"{len(medicoes_para_criar)} medições inseridas em lote via CSV.")

    return {
        "total_linhas_arquivo": total_linhas_processadas,
        "total_linhas_importadas": len(medicoes_para_criar),
        "erros": erros
    }
