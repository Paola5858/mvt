import datetime
import json
import random
import time
import warnings
import paho.mqtt.client as mqtt

warnings.filterwarnings("ignore", category=DeprecationWarning)



from decouple import config

MQTT = {
    "HOST": config("MQTT_HOST", default="localhost"),
    "PORT": config("MQTT_PORT", default=1883, cast=int),
    "KEEPALIVE": 60,
    "TOPIC": config("MQTT_TOPIC", default="dadosSensor"),
    "CLIENT_ID": config("MQTT_CLIENT_ID", default="django-publisher"),
    "USERNAME": config("MQTT_USERNAME", default=""),
    "PASSWORD": config("MQTT_PASSWORD", default=""),
}


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao MQTT com sucesso!")
    else:
        print(f"Erro na conexao: {rc}")


client = mqtt.Client(client_id=MQTT["CLIENT_ID"])
client.username_pw_set(MQTT["USERNAME"], MQTT["PASSWORD"])
client.on_connect = on_connect
client.connect(MQTT["HOST"], MQTT["PORT"], MQTT["KEEPALIVE"])
client.loop_start()

try:
    while True:
        quantidade_registros = 3

        payload_lista = []
        for _ in range(quantidade_registros):
            payload = {
                "valor": round(random.uniform(20, 35), 2),
                "medicaoid": random.randint(1, 3),
                "veiculoid": random.randint(1, 2),
                "data": datetime.datetime.now().isoformat()
            }
            payload_lista.append(payload)

        mensagem = json.dumps(payload_lista)
        client.publish(MQTT["TOPIC"], mensagem)

        print(f"Enviado: {mensagem}")

        time.sleep(5)

except KeyboardInterrupt:
    print("Encerrando...")

finally:
    client.loop_stop()
    client.disconnect()