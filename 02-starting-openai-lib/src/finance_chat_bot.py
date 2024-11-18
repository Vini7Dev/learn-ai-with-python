import json
import openai
import yfinance as yf

CHAT_GPT_MODEL = 'gpt-3.5-turbo-0125'
TEMPERATURE = 0
MAX_TOKENS = 1000
TOOLS = [{
    'type': 'function',
    'function': {
        'name': 'get_finance_info',
        'description': 'Retornar a cotação diária histórica para uma ação da bovespa',
        'parameters': {
            'type': 'object',
            'required': ['ticker', 'period'],
            'properties': {
                'ticker': {
                    'type': 'string',
                    'description': 'O ticker da ação. Exemplo: "AMEV3" para ambev, "PETR4" para petrobras, etc'
                },
                'period': {
                    'type': 'string',
                    'description': 'O período que serão retornados os dados históricos, sendo 1mo equivalente à 1 mês de dados, 1d à 1 dia e 1y à 1 ano',
                    'enum': ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
                }
            }
        }
    }
}]

# Tools

def get_finance_info(ticker, period):
    ticker_obj = yf.Ticker(f'{ticker}.SA')
    hist = ticker_obj.history(period=period)
    if (len(hist) > 30):
        slice_size = int(len(hist) / 30)
        hist = hist.iloc[::-slice_size][::-1]
    # hist.index = hist.index.strftime('%Y-%m-%d')
    hist = round(hist, 2)
    return hist['Close'].to_json()

available_tool_functions = {
    'get_finance_info': get_finance_info,
}

# Utils

def last_item(array):
    return array[len(array) - 1]

# Execution

def add_user_message(messages):
    user_message = input('[0 to Exit] User: ')

    messages.append({ 'role': 'user', 'content': user_message })

    return messages

def add_tool_calls_messages(messages, tool_calls):
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        function_to_call = available_tool_functions[function_name]
        function_response = function_to_call(
            ticker= function_args.get('ticker'),
            period= function_args.get('period'),
        )
        messages.append({
            'tool_call_id': tool_call.id,
            'role': 'tool',
            'name': function_name,
            'content': function_response,
        })

    return messages

def add_gpt_message(messages, client):
    chat_response = client.chat.completions.create(
        model=CHAT_GPT_MODEL,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        tools=TOOLS,
        tool_choice="auto",
        messages=messages,
    )

    tool_calls = chat_response.choices[0].message.tool_calls

    if (tool_calls):
        messages.append(chat_response.choices[0].message)

        messages = add_tool_calls_messages(messages=messages, tool_calls=tool_calls)

        return add_gpt_message(messages=messages, client=client)

    messages.append({
        'role': 'assistant', 'content': chat_response.choices[0].message.content,
    })

    return messages

def execute_chat(api_key):
    client = openai.Client(api_key=api_key)

    chat_messages = []

    while True:
        chat_messages = add_user_message(messages=chat_messages)

        if (last_item(chat_messages)['content'] == '0'): break

        chat_messages = add_gpt_message(messages=chat_messages, client=client)

        print(f'Assistant: {last_item(chat_messages)['content']}')

    return chat_messages
