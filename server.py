from flask import Flask, request, jsonify
import google.generativeai as genai
import os
import hvac

app = Flask(__name__)

client = hvac.Client(
    url=os.environ['VAULT_ADDR'],
    token=os.environ['VAULT_TOKEN'],
)
secret_response = client.secrets.kv.v2.read_secret_version(path='python-test-server-leak-50c87de5')

# Gemini API key (EXPOSED FOR TESTING PURPOSES)
GEMINI_API_KEY = secret_response['data']['data']['secret']
MODEL_NAME = "gemini-2.5-flash"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name=MODEL_NAME)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "No message provided."}), 400
    try:
        response = model.generate_content(user_message)
        bot_reply = getattr(response, "text", "")
        return jsonify({"reply": bot_reply})
    except Exception as e:
        return jsonify({"error": "Gemini SDK error.", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)