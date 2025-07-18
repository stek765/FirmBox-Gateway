# mqtt_publisher.py:
# Utilizzo di mqtt per pubblicare i log su un broker MQTT (che sarà sul ricevitore)
import paho.mqtt.client as mqtt 
import time

BROKER = "localhost"              # broker MQTT
PORT = 1883                       # porta MQTT
TOPIC = "firmbox/logs/device01"   # topic MQTT

LOG_FILE = "logs/data.log" 

# tail_f è una funzione che legge il file di log e lo pubblica su mqtt
def tail_f(filepath):
    with open(filepath, "r") as f:
        f.seek(0, 2)  # vai alla fine del file per leggere i dati piu recenti e in tempo reale
        while True:
            line = f.readline() # leggo una riga del file
            if not line:
                time.sleep(0.5) 
                continue
            yield line.strip() # ritorno la riga senza spazi bianchi

def main():
    client = mqtt.Client()    # creo un client MQTT
    client.connect(BROKER, PORT, 60) # connetto il client al broker
    client.loop_start() # avvio il loop del client

    print(f"\n- - - - - - - - - - - - - - - - - - - -\nCollegato a MQTT su {BROKER}:{PORT}, pubblicazione su '{TOPIC}'\n- - - - - - - - - - - - - - - - - - - -\n") # stampo il messaggio di connessione

    # leggo il file di log e lo pubblico su mqtt
    # line è di tipo stringa e legge una riga del file di log ogni volta
    for line in tail_f(LOG_FILE):  
        print("Invio MQTT:", line) # log dell'invio
        client.publish(TOPIC, line) # pubblico il dato su mqtt

if __name__ == "__main__":
    main()
