# command_subscriber.py:
# riceve i comandi che il browser invia al broker mqtt, ed esegue le azioni richieste passandole per seriale alla STM32
# (raspberry pi -> UART -> STM32)

import serial
import paho.mqtt.client as mqtt

BROKER = "localhost"   # si collega al broker mqtt (topic: firmbox/commands) a cui il pc invia i comandi
PORT = 1883
BAUD = 9600

TOPIC = "firmbox/commands"
SERIAL_PORT = "/dev/ttys014"  # porta seriale collegata alla STM32 (modifica secondo la tua configurazione)

# Apri la seriale una volta sola
ser = serial.Serial(SERIAL_PORT, BAUD, timeout=1)

# ricevo il comando MQTT e lo inoltro via UART alla STM32:
def on_message(client, userdata, msg):
    command = msg.payload.decode()
    print("Ricevuto comando:", command)
    if command == "led_on":
        # Accendo il LED sulla STM32
        print("Accendo il LED!")
        ser.write(b'LED_ON\n')  # Invia comando alla STM32
    elif command == "led_off":
        # Spengo il LED sulla STM32
        print("Spengo il LED!")
        ser.write(b'LED_OFF\n')
    elif command == "read":
        # Richiedo una lettura immediata del sensore
        print("Lettura sensore richiesta!")
        ser.write(b'READ\n')
    elif command == "reset":
        # Richiedo il reset del sensore
        print("Reset sensore richiesto!")
        ser.write(b'RESET\n')
    else:
        # Comando sconosciuto
        print("Comando sconosciuto:", command)

# main:
# Creo un client MQTT, mi connetto al broker e mi iscrivo al topic dei comandi
client = mqtt.Client()              # creo un client MQTT
client.connect(BROKER, PORT, 60)    # connetto il client al broker
client.subscribe(TOPIC)             # iscrivo al topic MQTT

client.on_message = on_message      # chiama on_message quando ricevo un messaggio
print(f"Ascolto comandi su {TOPIC}...")
client.loop_forever()