# command_subscriber.py
# Riceve comandi MQTT e li inoltra alla STM32 via UART

import serial
import paho.mqtt.client as mqtt

BROKER = "localhost"       # Broker MQTT
PORT = 1883                # Porta MQTT
BAUD = 115200              # Baud della STM32
TOPIC = "firmbox/commands" # Topic dei comandi
SERIAL_PORT = "/dev/serial0" # Porta seriale Raspberry→STM32 (es. GPIO14–15)

# Inizializza la seriale (una volta sola)
ser = serial.Serial(SERIAL_PORT, BAUD, timeout=1)

# Quando arriva un comando MQTT
def on_message(client, userdata, msg):
    command = msg.payload.decode().strip()
    print("Ricevuto comando MQTT:", command)

    # Invia lo stesso comando alla STM32
    serial_command = command.upper() + "\n"  # es. "LED_ON\n"
    ser.write(serial_command.encode())
    print("Inviato alla STM32:", serial_command.strip())

# Setup MQTT
client = mqtt.Client()
client.connect(BROKER, PORT, 60)
client.subscribe(TOPIC)
client.on_message = on_message

print(f"[MQTT] In ascolto su '{TOPIC}'... inoltro comandi alla STM32 via UART.")
client.loop_forever()