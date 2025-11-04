from flask import Flask, request, jsonify
import google.generativeai as genai
import boto3

app = Flask(__name__)

# Gemini API key (EXPOSED FOR TESTING PURPOSES)
# Define SSM parameter details
SSM_PARAMETER_NAME = '/chethanreddy123-python-test-server-app.py'
SSM_REGION = 'eu-north-1'

# Create an SSM client
ssm_client = boto3.client('ssm', region_name=SSM_REGION)

# Fetch the SecureString parameter with decryption
response = ssm_client.get_parameter(
    Name=SSM_PARAMETER_NAME,
    WithDecryption=True
)
GEMINI_API_KEY = response['Parameter']['Value']
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