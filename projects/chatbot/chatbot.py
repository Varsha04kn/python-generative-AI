# chatbot.py — Using Gemma (no system_instruction support)

import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('GEMINI_API_KEY')
if not API_KEY:
    raise ValueError('GEMINI_API_KEY not found.')

client = genai.Client(api_key=API_KEY)

MODEL_NAME = 'gemini-2.0-flash'

SYSTEM_PROMPT = '''You are a helpful, friendly, and concise AI assistant.
You answer questions clearly and ask for clarification when needed.
Keep responses under 200 words unless a longer answer is necessary.'''

history = []

def chat(user_input: str) -> str:
    global history

    history.append(types.Content(
        role="user",
        parts=[types.Part.from_text(text=user_input)]
    ))

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=history,
        config=types.GenerateContentConfig(
            temperature=0.7,
            system_instruction=SYSTEM_PROMPT
        )
    )

    reply = response.text

    history.append(types.Content(
        role="model",
        parts=[types.Part.from_text(text=reply)]
    ))

    return reply

def main():
    print('=' * 50)
    print(' Gemini AI Chatbot (Gemma) | Type exit to quit')
    print('=' * 50)
    while True:
        user_input = input('You: ').strip()
        if not user_input:
            continue
        if user_input.lower() in ('exit', 'quit', 'bye'):
            print('Bot: Goodbye! Have a great day.')
            break
        try:
            reply = chat(user_input)
            print(f'Bot: {reply}\n')
        except Exception as e:
            print(f'Bot: [Error] {e}\n')

if __name__ == '__main__':
    main()
