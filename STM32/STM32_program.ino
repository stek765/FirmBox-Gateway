String comando = "";         // Comando ricevuto via UART
bool led_state = false;      // Stato attuale del LED
bool blinking = false;       // Se il LED lampeggia
unsigned long lastBlink = 0; // Timestamp ultimo lampeggio

void setup() {
  Serial.begin(115200);      // UART per comunicare con il Raspberry Pi
  pinMode(PB0, OUTPUT);      // LED collegato al pin PB0
}

void loop() {
  // Leggi valore dalla fotoresistenza (collegata a PA0)
  int valore = analogRead(PA0);
  Serial.print("Luce: ");
  Serial.println(valore);

  // Controllo ricezione da UART
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      comando.trim();                // Rimuove spazi bianchi extra
      gestisciComando(comando);      // Esegue il comando
      comando = "";                  // Resetta il buffer comando
    } else {
      comando += c;                  // Aggiunge carattere al comando
    }
  }

  // Se attivo il lampeggio automatico
  if (blinking && millis() - lastBlink > 500) {
    led_state = !led_state;
    digitalWrite(PB0, led_state ? HIGH : LOW);
    lastBlink = millis();
  }

  delay(100); // Frequenza lettura fotoresistenza
}

void gestisciComando(String cmd) {
  if (cmd == "LED_ON") {
    blinking = false;
    digitalWrite(PB0, HIGH);
    led_state = true;
    Serial.println("LED acceso.");
  } 
  else if (cmd == "LED_OFF") {
    blinking = false;
    digitalWrite(PB0, LOW);
    led_state = false;
    Serial.println("LED spento.");
  } 
  else if (cmd == "BLINK") {
    blinking = true;
    Serial.println("LED lampeggia.");
  } 
  else if (cmd == "STATUS") {
    Serial.print("LED: ");
    Serial.println(led_state ? "ON" : "OFF");
  } 
  else {
    Serial.println("Comando sconosciuto.");
  }
}