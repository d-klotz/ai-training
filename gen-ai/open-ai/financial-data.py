import json

import openai
from dotenv import load_dotenv, find_dotenv
import yfinance as yf

_ = load_dotenv(find_dotenv())
client = openai.Client()

def get_historical_data(ticker, period='1mo'):
    ticker = ticker.replace('.SA', '')
    ticket_obj = yf.Ticker(f'{ticker}.SA')
    hist = ticket_obj.history(period=period)['Close']
    hist.index = hist.index.strftime('%Y-%m-%d')
    hist = round(hist, 2)

    if len(hist) > 30:
        slice_size = int(len(hist) // 30)
        hist = hist.iloc[::-slice_size][::-1]

    return hist.to_json()


tools = [
    {
        'type': 'function',
        'function': {
            'name': 'get_historical_data',
            'description': 'Get historical data for a given stock ticker',
            'parameters': {
                'type': 'object',
                'properties': {
                    'ticker': {
                        'type':'string',
                        'description': 'Stock ticker symbol, example: "ABEV3" for ambev, "PETR4" for petrobras, etc.'
                    },
                    'period': {
                        'type':'string',
                        'description': 'Historical period, example: "1mo" for one month, "3y" for three years, "1d" for one day, etc.',
                        'default': '1mo',
                        'enum': ['1mo', '3mo', '6mo', '1y', '2y', '5y', '1d', '5d', 'ytd', 'max']
                    }
                }
            }
        }
    }
]

available_functions = {'get_historical_data': get_historical_data}

def generate_answer():
    answer = client.chat.completions.create(
        messages=messages,
        model='gpt-4o-mini',
        tools=tools,
        tool_choice='auto'
    )

    tool_calls = answer.choices[0].message.tool_calls

    if tool_calls:
        messages.append(answer.choices[0].message)
        for call in tool_calls:
            func_name = call.function.name
            function_to_call = available_functions[func_name]
            func_args = json.loads(call.function.arguments)
            func_return = function_to_call(**func_args)
            messages.append({
                'tool_call_id': call.id,
                'role': 'tool',
                'name': func_name,
                'content': func_return,
            })
        second_answer = client.chat.completions.create(
            messages=messages,
            model='gpt-4o-mini',
        )
        messages.append(second_answer.choices[0].message)
    print(f"Assistant: {messages[-1].content}")
    return messages

if __name__ == "__main__":
    print('Welcome to the Stock Market Assistant! Type your question below and press Enter. Type "exit" to quit. \n')
    while True:
        user_input = input('User:')
        messages = [
            {
                'role': 'user',
                'content': user_input
            }
        ]
        messages = generate_answer()


