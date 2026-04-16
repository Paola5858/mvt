import logging
from datetime import datetime
from django.db import transaction
from api_telemetria.models import MedicaoVeiculo, Veiculo, Medicao

logger = logging.getLogger(__name__)


def processar_medicoes_mqtt(dados_medicao_list):
    """
    Processa uma lista de dados de medição recebidos via MQTT.
    Realiza inserção em lote e trata erros de forma robusta.
    """
    if not dados_medicao_list:
        logger.info("Nenhum dado de medição para processar via MQTT.")
        return

    veiculos_cache = {v.id: v for v in Veiculo.objects.all()}  # type: ignore
    medicoes_cache = {m.id: m for m in Medicao.objects.all()}  # type: ignore

    medicoes_para_criar = []
    erros_processamento = []

    for item in dados_medicao_list:
        try:
            try:
                veiculo_id = int(item["veiculoid"])
            except (KeyError, TypeError, ValueError):
                raise ValueError("veiculoid ausente ou inválido")

            try:
                medicao_id = int(item["medicaoid"])
            except (KeyError, TypeError, ValueError):
                try:
                    medicao_id = int(item["sensorid"])
                except (KeyError, TypeError, ValueError):
                    raise ValueError("medicaoid/sensorid ausente ou inválido")

            try:
                valor = float(item["valor"])
            except (KeyError, TypeError, ValueError):
                raise ValueError("valor ausente ou inválido")

            if veiculo_id not in veiculos_cache:
                raise ValueError(f"Veículo {veiculo_id} não encontrado.")
            if medicao_id not in medicoes_cache:
                raise ValueError(f"Medição {medicao_id} não encontrada.")

            data_str = item.get("data", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            data_convertida = datetime.strptime(data_str, "%Y-%m-%dT%H:%M:%S.%f")

            medicoes_para_criar.append(
                MedicaoVeiculo(
                    veiculo=veiculos_cache[veiculo_id],
                    medicao=medicoes_cache[medicao_id],
                    data=data_convertida,
                    valor=valor,
                )
            )
        except (ValueError, TypeError, KeyError) as e:
            erros_processamento.append(f"Erro ao processar item {item}: {e}")
            logger.error(f"Erro ao processar item MQTT: {item} - {e}")
        except Exception as e:
            erros_processamento.append(f"Erro inesperado ao processar item {item}: {e}")
            logger.critical(f"Erro crítico no processamento MQTT: {item} - {e}")

    if medicoes_para_criar:
        with transaction.atomic():
            MedicaoVeiculo.objects.bulk_create(medicoes_para_criar, batch_size=1000)
            logger.info(f"{len(medicoes_para_criar)} medições inseridas em lote via MQTT.")

    if erros_processamento:
        logger.warning(f"{len(erros_processamento)} erros encontrados durante o processamento MQTT.")

    return {"sucesso": len(medicoes_para_criar) > 0, "erros": erros_processamento}