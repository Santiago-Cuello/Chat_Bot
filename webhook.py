import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

PHONE_NUMBER_ID = "621297494409962"
GRAPH_URL = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"
ACCESS_TOKEN = "EAAKh98ZAwP0wBOZBR6hdCKqCJjyJJaZCHaZB86D1t91oM24C68iENtYheeOdb5MxHkflTphqnG1fQuiYWKmQbp5k4mjZB7hBZBD1nK8Mia2xzk9oGg9MJPSXWaWUuYXd9wu3FSJF4JYLRsD5cChJxZB9IG5ZAd85ZC2UuAC2tUBKhmdgWamdhx4wJQ5KZBw7sX4ee00u6CMLXuLohg1YfiNlEYPZAYaOZCgicZB55Uh1nYkaghNkc9ZAUZD"

def enviar_mensaje(numero, texto):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "text",
        "text": {"body": texto}
    }
    response = requests.post(GRAPH_URL, headers=headers, json=data)
    return response.json()

@app.route("/", methods=["GET"])
def home():
    return "Servidor WhatsApp Bot activo 🚀", 200

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Verificación de Webhook
        verify_token = "mi_token_de_verificacion"
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if mode == "subscribe" and token == verify_token:
            return challenge, 200
        else:
            return "Verificación fallida", 403

    if request.method == "POST":
        data = request.get_json()
        if data and "entry" in data:
            for entry in data["entry"]:
                for change in entry["changes"]:
                    value = change["value"]
                    messages = value.get("messages")
                    if messages:
                        msg = messages[0]
                        texto = msg["text"]["body"]
                        numero = msg["from"]

                        if "hola" in texto.lower():
                            respuesta = "¡Hola! ¿En qué puedo ayudarte hoy?"
                        elif "viaje" in texto.lower():
                            respuesta = "¿Desde dónde salís y hacia dónde querés ir?"
                        elif "gracias" in texto.lower():
                            respuesta = "¡De nada! 😊"
                        else:
                            respuesta = "No entendí eso. Escribí 'viaje' o 'hola'."

                        enviar_mensaje(numero, respuesta)

        return jsonify({"status": "ok"}), 200
@app.route("/", methods=["GET"])
def home():
    return "Servidor WhatsApp Bot activo 🚀", 200
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
