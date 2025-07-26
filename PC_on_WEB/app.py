# app.py:
# web dashboard per visualizzare i log del sensore e inviare comandi al sensore

from flask import Flask, render_template, jsonify, request
import threading
import paho.mqtt.client as mqtt
import os

app = Flask(__name__)

# Variabile globale per i dati ricevuti
latest_data = []

# Funzione callback per MQTT
def on_message(client, userdata, msg):
    global latest_data  # variabile per salvare i dati ricevuti
    print("Ricevuto MQTT:", msg.payload.decode())
    latest_data.append(msg.payload.decode())
    # Limita la lunghezza della lista
    if len(latest_data) > 100:
        latest_data = latest_data[-100:]

def mqtt_thread():
    print("MQTT thread avviato")
    client = mqtt.Client(client_id="flask_dashboard")
    client.connect("192.168.5.122", 1883, 60)  # IP del Raspberry Pi
    client.subscribe("firmbox/logs/device01")
    client.on_message = on_message
    client.loop_forever()

# Avvia il thread MQTT solo se il processo è quello principale
if __name__ == "__main__" and os.environ.get("WERKZEUG_RUN_MAIN") != "true":
    threading.Thread(target=mqtt_thread, daemon=True).start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/logs")
def logs_page():
    return render_template("logs.html")

# /api/logs: restituisce i dati ricevuti da MQTT
@app.route("/api/logs")
def api_logs():
    return jsonify(latest_data)

# /command: invia un comando al sensore via MQTT
@app.route("/command", methods=["POST"])
def command():
    data = request.get_json()
    cmd = data.get("command")
    if not cmd:
        return {"status": "Nessun comando ricevuto"}, 400
    try:
        import paho.mqtt.publish as publish
        publish.single("firmbox/commands", cmd, hostname="192.168.5.122") # si collega al broker mqtt (topic: firmbox/commands) 
        return {"status": f"Comando '{cmd}' inviato"}
    except Exception as e:
        return {"status": f"Errore invio comando: {e}"}, 500

if __name__ == "__main__":
    app.run(debug=False, port=5000)