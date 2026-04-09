import uuid
import os
import json
import django
import paho.mqtt.client as mqtt
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")
django.setup()

from django.conf import settings  # noqa: E402
from api_telemetria.models import MedicaoVeiculo, Veiculo, Medicao  # noqa: E402


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"[MQTT] Falha na conexão: {reason_code}")
        client.disconnect()
    else:
        topic = settings.MQTT.get("TOPIC", "dadosSensor")
        client.subscribe(topic)
        print(f"[MQTT] Conectado! Inscrito no tópico: {topic}")


def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)

        print(f"[MQTT] Mensagem recebida: {data}")

        veiculo_id = int(data["veiculoid"])
        medicao_id = int(data.get("medicaoid") or data["sensorid"])
        valor = float(data["valor"])
        data_raw = data.get("data", datetime.now().isoformat())
        data_str = datetime.fromisoformat(data_raw).strftime("%Y-%m-%d")

        veiculo = Veiculo.objects.get(id=veiculo_id)
        medicao = Medicao.objects.get(id=medicao_id)

        MedicaoVeiculo.objects.create(
            veiculo=veiculo,
            medicao=medicao,
            data=data_str,
            valor=valor,
        )

        print(f"[MQTT] Salvo: veiculo={veiculo_id} medicao={medicao_id} valor={valor}")

    except KeyError as e:
        print(f"[ERRO] Campo obrigatório ausente no payload: {e}")
    except Veiculo.DoesNotExist:
        print(f"[ERRO] Veículo {veiculo_id} não encontrado no banco")
    except Medicao.DoesNotExist:
        print(f"[ERRO] Medição {medicao_id} não encontrada no banco")
    except Exception as e:
        print(f"[ERRO] Falha ao processar mensagem: {e}")


def on_disconnect(client, userdata, disconnect_flags, reason_code, properties):
    if reason_code.value != 0:
        print(f"[MQTT] Desconectado inesperadamente: {reason_code}. Tentando reconectar...")
    else:
        print("[MQTT] Desconectado normalmente.")


def main():
    mqtt_cfg = settings.MQTT

    host = mqtt_cfg.get("HOST", "127.0.0.1")
    port = mqtt_cfg.get("PORT", 1883)
    keepalive = mqtt_cfg.get("KEEPALIVE", 60)
    client_id = mqtt_cfg.get("CLIENT_ID", f"django-worker-{uuid.uuid4().hex[:8]}")
    username = mqtt_cfg.get("USERNAME")
    password = mqtt_cfg.get("PASSWORD")

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)

    if username and password:
        client.username_pw_set(username, password)


    client.reconnect_delay_set(min_delay=1, max_delay=30)

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    print(f"[MQTT] Conectando em {host}:{port}...")
    client.connect(host, port, keepalive)

    client.loop_forever()


if __name__ == "__main__":
    main()
