# sender.py:
# invia dati fake del sensore verso il ricevitore (uart_reader.py)
# (per testare il sistema non è usato nel sistema reale)

import serial
import time
import random

# Configura la porta virtuale dove il ricevitore (uart_reader.py) sta ascoltando
PORT = '/dev/ttys015'  # cambia in base alla tua configurazione socat
BAUD = 9600

def generate_fake_data():
    temperature = round(random.uniform(20.0, 30.0), 2)
    humidity = round(random.uniform(30.0, 70.0), 2)
    # temperatura e umidità sono randomici tra 20 e 30 e 30 e 70
    return f"temperature={temperature}C humidity={humidity}%"

def main():
    ser = serial.Serial(PORT, BAUD)
    print(f"Invio dati su {PORT} a {BAUD} baud...")

    print("\ndevice01: ")
    while True:
        try:
            msg = generate_fake_data() # genero il dato in maniera randomica
            ser.write((msg + '\n').encode()) # lo invio con utf-8
            print("Inviato ->", msg)
            time.sleep(3) # aspetto 3 sec
        except KeyboardInterrupt:
            print("Interrotto.")
            break
        except Exception as e:
            print("Errore:", e)
            break

if __name__ == "__main__":
    main()
