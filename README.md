
# Simple Gemini Chatbot Backend

This is a test repository to demonstrate scanning for exposed API keys.

## Usage

- The Gemini API key is intentionally exposed in the code for testing purposes.
- Install dependencies:
	```bash
	pip install flask requests
	```
- Run the server:
	```bash
	python server.py
	```

## Endpoints

- `/chat` - POST endpoint for chatbot messages. Send JSON: `{ "message": "your text" }`

## Warning

**Do not use this code in production. The Gemini API key is exposed for testing only.**
