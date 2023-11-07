import asyncio
from characterai import PyAsyncCAI

async def main():
    client = PyAsyncCAI('19a703af5bf8b29673514f8afd0041c775cd5916')

    char = input('Enter CHAR: ')
    unique_id = input('Enter Unique Chat ID: ')

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

        while True:
            message = input('You: ')

            data = await chat2.send_message(char, unique_id, message, author)

            name = data['turn']['author']['name']
            text = data['turn']['candidates'][0]['raw_content']

            print(f"{name}: {text}")

asyncio.run(main())