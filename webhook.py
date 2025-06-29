import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

ACCESS_TOKEN = "TU_TOKEN_DE_ACCESO"
PHONE_NUMBER_ID = "621297494409962"
GRAPH_URL = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"

VERIFY_TOKEN = "mi_token_de_verificacion"

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
    r = requests.post(GRAPH_URL, headers=headers, json=data)
    print("🟢 Enviado a:", numero)
    print("📤 Respuesta:", r.status_code, r.text)
    return r.json()

@app.route("/", methods=["GET"])
def index():
    return "¡Servidor WhatsApp Bot activo!", 200

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Token inválido", 403

    if request.method == "POST":
        data = request.get_json()
        print("📨 Datos recibidos:", data)

        if data and "entry" in data:
            for entry in data["entry"]:
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    messages = value.get("messages")

                    if messages:
                        message = messages[0]
                        texto = message["text"]["body"]
                        numero = message["from"]

                        # Lógica de respuesta simple
                        if "hola" in texto.lower():
                            respuesta = "¡Hola! ¿En qué puedo ayudarte?"
                        elif "gracias" in texto.lower():
                            respuesta = "¡De nada! 😊"
                        else:
                            respuesta = "No entendí eso. Escribí 'hola' o 'gracias'."

                        enviar_mensaje(numero, respuesta)

        return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
