import openai
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
client = openai.Client()
messages = []

while True:
    user_input = input()
    messages.append({'role': 'user', 'content': user_input})
    answer = client.chat.completions.create(
        messages=messages,
        model='gpt-4o-mini',
        max_tokens=1000,
        temperature=0,
        stream=True)

    full_answer = ''
    print('Astro:')
    for stream_message in answer:
        text = stream_message.choices[0].delta.content
        if text:
            full_answer += text
            print(text, end='')

    messages.append({'role': 'assistant', 'content': full_answer})
    print('\n')