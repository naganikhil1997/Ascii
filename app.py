from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)

# Get the API key from environment variables
XAI_API_KEY = os.getenv('XAI_API_KEY')

# Define the endpoint for chatting
@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Get the input message from the request
        user_message = request.json.get('message')
        
        # Prepare the payload for x.ai API
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are Grok, a chatbot inspired by the Hitchhikers Guide to the Galaxy."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            "model": "grok-beta",
            "stream": False,
            "temperature": 0
        }

        # Send the request to the x.ai API
        response = requests.post(
            "https://api.x.ai/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {XAI_API_KEY}"
            },
            json=payload
        )

        # Check if the response is successful
        if response.status_code == 200:
            data = response.json()
            answer = data['choices'][0]['message']['content']
            return jsonify({"answer": answer}), 200
        else:
            return jsonify({"error": "Failed to get response from x.ai API"}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)