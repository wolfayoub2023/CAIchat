import asyncio
from characterai import PyAsyncCAI
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

async def chatbot_logic(char, unique_id, message):
    client = PyAsyncCAI('19a703af5bf8b29673514f8afd0041c775cd5916')

    author_id = '284241435'

    async with client.connect() as chat2:
        try:
            # Attempt to get the chat history with the provided chat_id
            chat_history = await client.chat2.get_history(unique_id)

            if chat_history:
                print(f"Accessing existing chat with ID: {unique_id}")
            else:
                raise Exception("Chat does not exist")
        except Exception:
            # If the chat with the provided ID does not exist, create a new chat
            response, answer = await chat2.new_chat(char, unique_id, author_id)
            print(f"Created a new chat with ID: {unique_id}")

        author = {
            'author_id': author_id  # Use the same author ID for messages in the chat
        }

        message_data = await chat2.send_message(char, unique_id, message, author)

        name = message_data['turn']['author']['name']
        text = message_data['turn']['candidates'][0]['raw_content']

        return f"{name}: {text}"

@app.route('/', methods=['POST'])
def chatbot_endpoint():
    try:
        data = request.get_json()
        char = data['char']
        unique_id = data['unique_id']
        message = data['message']

        response_text = asyncio.run(chatbot_logic(char, unique_id, message))
        
        # Extract the message text
        message_text = response_text.split(': ', 1)[-1]
        
        return jsonify({'response': message_text})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
