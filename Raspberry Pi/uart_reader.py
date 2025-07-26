# uart_reader.py:
# simula il ricevitore del sensore, che:
    # 1. Leggi la porta seriale
    # 2. Leggi i dati in arrivo
    # 3. Logga e firma i dati
    # 4. Salva i dati in un file
    # 5. Salva le firme in un altro file
    
import serial 
import time
import hashlib
import os

os.makedirs("logs", exist_ok=True)

PORT = '/dev/serial0' # porta seriale per ricevere dall'smt32
BAUD = 115200 # baud rate = bit trasmessi in un secondo

MAX_SIZE = 1024 * 1024 # 1 MB

LOG_FILE = "logs/data.log" # file per i log
SIG_FILE = "logs/data.sig" # file per le signature (hash SHA256)

# funzione per pulire i log ogni 1MB
def clear_if_too_large(file_path):
    """Svuota il file se supera MAX_SIZE."""
    if os.path.exists(file_path) and os.path.getsize(file_path) > MAX_SIZE:
        with open(file_path, "w") as f:
            f.truncate(0) #svuota il file
        print(f"[!] File > 1MB. Svuotato..")

def log_and_sign(data):
    """
    - Apro LOG_FILE e metto i log
    - Apro SIG_FILE e metto le signature
    """

    # svuoto se supera max size
    clear_if_too_large(LOG_FILE)
    clear_if_too_large(SIG_FILE)
    
    with open(LOG_FILE, "a") as log_file:
        timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]") # creo un timestamp per il dato
        log_formatted = f"{timestamp} {data}\n" # creo la riga di log con il suo timestamp
        
        log_file.write(log_formatted) # scrivo il log nel file
        print("LogFile:", log_formatted.strip()) # stampo il log
        

    with open(SIG_FILE, "a") as sig_file:
        hash_log = hashlib.sha256(log_formatted.encode())  # calcolo l'hash SHA256 del dato con timestamp e \n

        # scrivo la signature nel file
        sig_file.write(hash_log.hexdigest() + "\n") # hexdigest converte l'hash in esadecimale per questioni di spazio
        print("SigFile:", hash_log.hexdigest(), "\n- - - - - - - - - - - - - - - - - - - - - - - - - - - -\n") # stampo la signature

        
def main():
    """
    - Apro la porta seriale
    - Leggo i dati in arrivo e decodifico da bytes a stringa
    - Se la riga non è vuota, chiamo la funzione log_and_sign
    """
    # Apro la porta seriale
    ser = serial.Serial(PORT, BAUD, timeout=1)
    print("ascolto su", PORT, "a", BAUD, "baud...")

    
    while True:
        try: 
            # leggo i dati in arrivo fino a \n, 
            # decofico da bytes a stringa
            # rimuovo spazi bianchi e '\0'
            line = ser.readline().decode('utf-8', errors='ignore').strip()

            # se ho ricevuto qualcosa
            if line: 
                # lo stampo
                print(f"{time.time():.2f} -> {line}")
                log_and_sign(line) # chiamo la funzione log_and_sign
        
        except KeyboardInterrupt:
            print("Interrotto.") # se l'utente usa ctrl+c
            break
        except Exception as e:
            print("Errore", e) # se c'è un errore, lo stampo
            


if __name__ == "__main__":
    main()