# mqtt_subscriber.py:
# legge i log da mqtt e li salva nel file logs/shared_buffer.log (che è condiviso con il web dashboard)

import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883

TOPIC = "firmbox/logs/device01"           # topic MQTT
BUFFER_FILE = "logs/shared_buffer.log"    # file per salvare i log

# scrivo il log nel file logs/shared_buffer.log
def on_message(client, userdata, msg):
    with open(BUFFER_FILE, "a") as f:
        f.write(msg.payload.decode() + "\n")

def main():
    client = mqtt.Client()            # creo un client MQTT
    client.connect(BROKER, PORT, 60)  # connetto il client al broker

    client.subscribe(TOPIC)           # iscrivo al topic MQTT
    client.on_message = on_message    # chiama on_message quando ricevo un messaggio

    client.loop_forever()  # il client rimane in ascolto del topic MQTT

if __name__ == "__main__":
    main()