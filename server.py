import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Gemini API key (EXPOSED FOR TESTING PURPOSES)
GEMINI_API_KEY = "AIzaSyD-EXPOSED-FAKE-KEY-1234567890"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta2/models/chat-bison-001:generateMessage"

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "No message provided."}), 400

    payload = {
        "prompt": {
            "messages": [
                {"content": user_message}
            ]
        }
    }
    params = {"key": GEMINI_API_KEY}
    response = requests.post(GEMINI_API_URL, params=params, json=payload)
    if response.status_code == 200:
        data = response.json()
        bot_reply = data.get('candidates', [{}])[0].get('content', '')
        return jsonify({"reply": bot_reply})
    else:
        return jsonify({"error": "Gemini API error.", "details": response.text}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
