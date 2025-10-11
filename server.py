```python
import os
from flask import Flask, request, jsonify
import requests
import hvac
import sys

app = Flask(__name__)

# Initialize Vault client from environment variables and fetch the secret
try:
    client = hvac.Client()
    if not client.is_authenticated():
        print("Vault authentication failed. Check VAULT_ADDR and VAULT_TOKEN.", file=sys.stderr)
        sys.exit(1)
    
    secret_path = 'python-test-server-server-py-69437cd3'
    read_secret_response = client.secrets.kv.v2.read_secret_version(path=secret_path)
    GEMINI_API_KEY = read_secret_response['data']['data']['GEMINI_API_KEY']
except Exception as e:
    print(f"Error fetching secret from Vault: {e}", file=sys.stderr)
    sys.exit(1)

# Gemini API key (EXPOSED FOR TESTING PURPOSES)
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