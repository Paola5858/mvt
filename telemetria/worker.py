import os
import json
import django
import paho.mqtt.client as mqtt
import logging
from datetime import datetime

from django.conf import settings
from api_telemetria.models import Veiculo, Medicao
from api_telemetria.mqtt_service import processar_medicoes_mqtt

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")
django.setup()

logger = logging.getLogger(__name__)

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        logger.error(f"[MQTT] Falha na conexão: {reason_code}")
        client.disconnect()
    else:
        topic = settings.MQTT.get("TOPIC", "dadosSensor")
        client.subscribe(topic)
        logger.info(f"[MQTT] Conectado! Inscrito no tópico: {topic}")

def on_message(client, userdata, msg):
    """
    Chamado quando uma mensagem chega no tópico.
    O payload é um vetor (lista) de JSONs com dados de medição.
    Percorre cada item do vetor e chama salvar_medicao para cada um.
    """
    try:
        payload = msg.payload.decode("utf-8")
        dados = json.loads(payload)

        logger.info(f"[MQTT] Mensagem recebida com {len(dados)} registro(s)")

        # Processa os dados usando o novo serviço
        resultado = processar_medicoes_mqtt(dados)
        if resultado["erros"]:
            for erro in resultado["erros"]:
                logger.warning(f"[MQTT] Erro no processamento de item: {erro}")

    except json.JSONDecodeError as e:
        logger.error(f"[MQTT] Payload não é um JSON válido: {e}")
    except Exception as e:
        logger.critical(f"[MQTT] Falha ao processar mensagem: {e}")

def on_disconnect(client, userdata, disconnect_flags, reason_code, properties):
    if reason_code.value != 0:
        logger.warning(f"[MQTT] Desconectado inesperadamente: {reason_code}. Tentando reconectar...")
    else:
        logger.info("[MQTT] Desconectado normalmente.")

def main():
    # Configuração de logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    mqtt_cfg = settings.MQTT

    host = mqtt_cfg.get("HOST", "127.0.0.1")
    port = mqtt_cfg.get("PORT", 1883)
    keepalive = mqtt_cfg.get("KEEPALIVE", 60)
    client_id = mqtt_cfg.get("CLIENT_ID", f"django-worker-{os.getpid()}") # Usando PID para client_id
    username = mqtt_cfg.get("USERNAME")
    password = mqtt_cfg.get("PASSWORD")

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)

    if username and password:
        client.username_pw_set(username, password)

    client.reconnect_delay_set(min_delay=1, max_delay=30)

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    logger.info(f"[MQTT] Conectando em {host}:{port}...")
    try:
        client.connect(host, port, keepalive)
    except Exception as e:
        logger.critical(f"[MQTT] Erro ao conectar ao broker MQTT: {e}")
        return # Termina o worker se não conseguir conectar

    client.loop_forever()

if __name__ == "__main__":
    main()
