import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

PHONE_NUMBER_ID = "621297494409962"
GRAPH_URL = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
ACCESS_TOKEN = "EAAKh98Z..."

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

    print("📤 Enviando mensaje a:", numero)
    print("📨 Contenido:", texto)

    response = requests.post(GRAPH_URL, headers=headers, json=data)
    print("🔁 Respuesta API Meta:", response.status_code, response.text)

    return response.json()

@app.route("/", methods=["GET"])
def index():
    return "Bot de WhatsApp activo y funcionando", 200

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
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
        print("📥 Datos recibidos webhook:", data)

        if data and "entry" in data:
            for entry in data["entry"]:
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    messages = value.get("messages")

                    if messages:
                        msg = messages[0]
                        texto = msg["text"]["body"]
                        numero = msg["from"]

                        print("📬 Mensaje recibido de", numero, ":", texto)

                        # Respuesta según texto
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

if __name__ == "__main__":
    app.run(port=5000)
