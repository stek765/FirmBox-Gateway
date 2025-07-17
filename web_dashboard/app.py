# app.py:
# web dashboard per visualizzare i log del sensore e inviare comandi al sensore

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# /: pagina principale, che mostra il file index.html
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/logs")
def logs_page():
    return render_template("logs.html")


# /api/logs: pagina che mostra i log del sensore (carica gli ultimi 50 log)
@app.route("/api/logs")
def api_logs():
    try:
        with open("../pi_middleware/logs/shared_buffer.log") as f:
            lines = f.readlines()[-100:]  # ultimi 50 log
        return jsonify([line.strip() for line in lines])
    except FileNotFoundError:
        return jsonify([])


# /command: pagina che invia un comando al sensore (LED ON, LED OFF, RESET SENSOR, READ SENSOR)
@app.route("/command", methods=["POST"])
def command():
    # funziona così:
    # 1. Ricevo un comando POST
    # 2. Invio il comando al broker MQTT (con topic firmbox/commands)
    # 3. Restituisco un messaggio di successo o di errore
    data = request.get_json()
    cmd = data.get("command")
    if not cmd:
        return {"status": "Nessun comando ricevuto"}, 400
    try:
        import paho.mqtt.publish as publish
        publish.single("firmbox/commands", cmd, hostname="localhost")
        return {"status": f"Comando '{cmd}' inviato"}
    except Exception as e:
        return {"status": f"Errore invio comando: {e}"}, 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)