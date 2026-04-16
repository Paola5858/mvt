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

    veiculos_cache = {v.id: v for v in Veiculo.objects.all()}
    medicoes_cache = {m.id: m for m in Medicao.objects.all()}

    medicoes_para_criar = []
    erros_processamento = []

    for item in dados_medicao_list:
        try:
            veiculo_id = int(item.get("veiculoid"))
            medicao_id = int(item.get("sensorid"))
            valor = float(item.get("valor"))

            if veiculo_id not in veiculos_cache:
                raise ValueError(f"Veículo {veiculo_id} não encontrado.")
            if medicao_id not in medicoes_cache:
                raise ValueError(f"Medição {medicao_id} não encontrada.")

            data_str = item.get("data", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            # Padronizando para YYYY-MM-DD HH:MM:SS para consistência
            data_convertida = datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S")

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
    
    return {"total_processados": len(dados_medicao_list), "total_inseridos": len(medicoes_para_criar), "erros": erros_processamento}
