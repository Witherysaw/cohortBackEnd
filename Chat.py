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
