from dotenv import load_dotenv, find_dotenv

import openai

CHAT_GPT_MODEL = 'gpt-3.5-turbo-0125'
TEMPERATURE = 0
MAX_TOKENS = 1000

_ = load_dotenv(find_dotenv())

client = openai.Client()

def get_user_message():
    user_message = input('["0" para sair] User: ')

    return { 'message': { 'role': 'user', 'content': user_message } }

def get_gpt_response(messages, model=CHAT_GPT_MODEL, max_tokens=MAX_TOKENS, temperature=TEMPERATURE):
    chat_response = client.chat.completions.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=messages
    )

    chat_message = chat_response.choices[0].message.model_dump(exclude_none=True)

    return { 'message': chat_message, 'usage': chat_response.usage }

def get_usage(usages=[]):
    result = { 'prompt': 0, 'completion': 0, 'total': 0 }

    for usage in usages:
        result['prompt'] += usage.prompt_tokens
        result['completion'] += usage.completion_tokens
        result['total'] += usage.total_tokens

    print(f'===> result: {result}')

    return result

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

        print(f'Chat: {chat_response['message']['content']}')

    return {
        'messages': chat_messages,
        'usages': chat_usages,
        'usage_totals': get_usage(usages=chat_usages),
    }

execute_chat()
