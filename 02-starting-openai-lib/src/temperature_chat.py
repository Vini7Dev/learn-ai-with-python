import json

import openai

CHAT_GPT_MODEL = 'gpt-3.5-turbo-0125'
TEMPERATURE = 0
MAX_TOKENS = 1000
TOOLS = [{
    'type': 'function',
    'function': {
        'name': 'get_current_temperature',
        'description': 'Obtém a temperatura atual em cada cidade',
        'parameters': {
            'type': 'object',
            'required': ['city'],
            'properties': {
                'city': {
                    'type': 'string',
                    'description': 'O nome da cidade em formato de texto. Exemplo: São Paulo',
                },
                'unity': {
                    'type': 'string',
                    'enum': ['celcius', 'fahrenheit']
                },
            },
        },
    },
}]

# Tools

def get_current_temperature(city, unity='celcius'):
    city_lower = city.lower()

    temperatures = {
        'são paulo': 32,
        'porto alegre': 25,
        'rio de janeiro': 35,
    }

    return json.dumps(
        { 'city': city, 'unity': unity, 'temperature': temperatures.get(city_lower) or 'unknown' },
        ensure_ascii=False,
    )

available_tool_functions = {
    'get_current_temperature': get_current_temperature,
}

# Execution

def get_user_message(messages):
    user_message = input('["0" para sair] User: ')

    messages.append({ 'role': 'user', 'content': user_message })

    return messages

def get_gpt_response(messages, client):
    chat_response = client.chat.completions.create(
        model=CHAT_GPT_MODEL,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        tools=TOOLS,
        tool_choice="auto",
        messages=messages,
        #  stream=True,
    )

    messages.append(chat_response.choices[0].message)

    tool_calls = chat_response.choices[0].message.tool_calls

    if tool_calls:
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            function_to_call = available_tool_functions[function_name]
            function_response = function_to_call(
                city = function_args.get('city'),
                unity = function_args.get('unity'),
            )
            messages.append({
                'tool_call_id': tool_call.id,
                'role': 'tool',
                'name': function_name,
                'content': function_response,
            })

        return get_gpt_response(messages, client=client)

    messages.append({
        'role': 'assistant', 'content': chat_response.choices[0].message.content
    })

    return messages

def execute_chat(api_key):
    client = openai.Client(api_key=api_key)

    chat_messages = []

    while True:
        chat_messages = get_user_message(messages=chat_messages)

        if (chat_messages[len(chat_messages)-1]['content'] == '0'): break

        chat_messages = get_gpt_response(messages=chat_messages, client=client)

        print(f'Assistant: {chat_messages[len(chat_messages)-1]['content']}')

    return chat_messages
