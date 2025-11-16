from flask import Flask, request, jsonify
import google.generativeai as genai
import os
import hvac

app = Flask(__name__)

# Vault client initialization
vault_addr = os.environ['VAULT_ADDR']
vault_token = os.environ['VAULT_TOKEN']

client = hvac.Client(url=vault_addr, token=vault_token)
if not client.is_authenticated():
    raise Exception("Vault authentication failed. Check VAULT_ADDR and VAULT_TOKEN environment variables.")

# Fetch Gemini API key from Vault
vault_path = 'secret/data/chethanreddy123/python-test-server/app.py'
read_response = client.read(vault_path)

if not read_response:
    raise Exception(f"Secret not found at Vault path: {vault_path}")

# Assume secret data is nested under ['data']['data']['secret']
if 'data' not in read_response or 'data' not in read_response['data'] or 'secret' not in read_response['data']['data']:
    raise Exception(f"Secret data malformed at {vault_path}. Expected ['data']['data']['secret'].")

GEMINI_API_KEY_FROM_VAULT = read_response['data']['data']['secret']

# Gemini API key (EXPOSED FOR TESTING PURPOSES)
GEMINI_API_KEY = GEMINI_API_KEY_FROM_VAULT
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