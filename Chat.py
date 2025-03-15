from flask import Blueprint, request, jsonify
import openai
from flask_cors import CORS

# Initialize the chat blueprint
def create_chat_app():
    chat_bp = Blueprint('chat', __name__)
    CORS(chat_bp)

    # Directly using your OpenAI API key
    openai.api_key = "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"  # Replace with your API key

    @chat_bp.route('/chat', methods=['POST'])
    def chat():
        user_message = request.json.get('message')

        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        try:
            # Use the updated Chat API method
            client = openai.OpenAI(api_key=openai.api_key)

            response = client.chat.completions.create(
                model="gpt-4o-mini",  # Replace with the model you're using
                messages=[
                    {"role": "system", "content": "You are an AI assistant for AI-Solutions, a fictitious start-up company. You only answer questions related to AI-Solutions, its AI-powered virtual assistant, software solutions, and digital employee experience. If a question is unrelated, politely refuse to answer."},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=100
            )

            ai_response = response.choices[0].message.content

            return jsonify({'response': ai_response})

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return chat_bp
