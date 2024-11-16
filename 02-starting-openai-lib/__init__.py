from dotenv import load_dotenv, find_dotenv

import openai

CHAT_GPT_MODEL = 'gpt-3.5-turbo-0125'
TEMPERATURE = 0
MAX_TOKENS = 1000

_ = load_dotenv(find_dotenv())

client = openai.Client()

def print_chat(message, end=''):
    print(message, end=end)

def get_user_message():
    user_message = input('["0" para sair] User: ')

    return { 'message': { 'role': 'user', 'content': user_message } }

def get_gpt_response(messages, model=CHAT_GPT_MODEL, max_tokens=MAX_TOKENS, temperature=TEMPERATURE):
    chat_response_stream = client.chat.completions.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=messages,
        stream=True
    )

    chat_message_text = ''

    for chat_response in chat_response_stream:
        chat_delta_content = chat_response.choices[0].delta.content

        if chat_delta_content == None: continue

        chat_message_text += chat_delta_content

        print_chat(chat_delta_content)

    print_chat('', end='\n')

    chat_message = { 'role': 'assistant', 'content': chat_message_text }

    return { 'message': chat_message, 'usage': chat_response.usage }

'''
def get_usage(usages=[]):
    result = { 'prompt': 0, 'completion': 0, 'total': 0 }

    for usage in usages:
        result['prompt'] += usage.prompt_tokens
        result['completion'] += usage.completion_tokens
        result['total'] += usage.total_tokens

    return result
'''

def execute_chat():
    chat_messages = []
    chat_usages = []

    while(True):
        user_message = get_user_message()

        if (user_message['message']['content'] == '0'): break

        chat_messages.append(user_message['message'])

        chat_response = get_gpt_response(messages=chat_messages)

        chat_messages.append(chat_response['message'])

        chat_usages.append(chat_response['usage'])

    return {
        'messages': chat_messages,
        # 'usage_totals': get_usage(usages=chat_usages),
        'usages': chat_usages
    }

chat_result = execute_chat()

print(f'=======> chat_result: {chat_result}')
