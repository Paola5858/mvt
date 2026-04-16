import os
import json
import logging
import uuid
import warnings
import paho.mqtt.client as mqtt
from django.conf import settings
from api_telemetria.mqtt_service import processar_medicoes_mqtt
import django

warnings.filterwarnings("ignore", category=DeprecationWarning)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")


django.setup()


logger = logging.getLogger(__name__)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        topic = settings.MQTT.get("TOPIC", "dadosSensor")
        client.subscribe(topic)
        logger.info(f"[MQTT] Conectado! Inscrito no topico: {topic}")
    else:
        logger.error(f"[MQTT] Falha na conexao: {rc}")
        client.disconnect()


def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        dados = json.loads(payload)
        logger.info(f"[MQTT] Mensagem recebida com {len(dados)} registro(s)")
        resultado = processar_medicoes_mqtt(dados)
        if resultado and resultado.get("erros"):
            for erro in resultado["erros"]:
                logger.warning(f"[MQTT] Erro no processamento de item: {erro}")
    except json.JSONDecodeError as e:
        logger.error(f"[MQTT] Payload nao e um JSON valido: {e}")
    except Exception as e:
        logger.critical(f"[MQTT] Falha ao processar mensagem: {e}")


def on_disconnect(client, userdata, rc):
    if rc != 0:
        logger.warning(f"[MQTT] Desconectado inesperadamente: {rc}. Tentando reconectar...")
    else:
        logger.info("[MQTT] Desconectado normalmente.")


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    mqtt_cfg = settings.MQTT

    host = mqtt_cfg.get("HOST", "127.0.0.1")
    port = mqtt_cfg.get("PORT", 1883)
    keepalive = mqtt_cfg.get("KEEPALIVE", 60)
    client_id = mqtt_cfg.get("CLIENT_ID", f"django-worker-{uuid.uuid4().hex[:8]}")
    username = mqtt_cfg.get("USERNAME")
    password = mqtt_cfg.get("PASSWORD")

    client = mqtt.Client(client_id=client_id)

    if username and password:
        client.username_pw_set(username, password)

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    logger.info(f"[MQTT] Conectando em {host}:{port}...")
    try:
        result = client.connect(host, port, keepalive)
        logger.info(f"[MQTT] Connect result: {result}")
    except Exception as e:
        logger.critical(f"[MQTT] Erro ao conectar ao broker MQTT: {e}")
        return

    client.loop_forever()


if __name__ == "__main__":
    main()