import os
import requests

from transformers import AutoTokenizer

def execute():
    model = 'mistralai/Mixtral-8x7B-Instruct-v0.1'
    url = f'https://api-inference.huggingface.co/models/{model}'
    hugging_face_token = os.getenv('HUGGING_FACE_TOKEN')
    headers = {'Authorization': f'Bearer {hugging_face_token}'}

    '''
    chat = [
        { 'role': 'user', 'content': 'Olá, qual o seu nome?' },
        { 'role': 'assistant', 'content': 'Olá, eu sou um modelo de AI. Como posso ajudar?' },
        { 'role': 'user', 'content': 'Gostaria de apresnder Python. Você tem alguma dica?' },
    ]
    '''

    chat = []

    while True:
        user_message = input('(Q = Sair) Usuário: ')
        chat.append({'role': 'user', 'content': user_message})
        if user_message == 'Q':
            break

        tokenizer = AutoTokenizer.from_pretrained(model)
        chat_template = tokenizer.apply_chat_template(
            chat,
            tokenize=False,
            add_generation_prompt=True
        )
        json = {
            'options': {'use_cache': False, 'wait_for_model': True},
            'parameters': {'max_new_tokens': 100},
            'inputs': chat_template,
        }
        response = requests.post(url, json=json, headers=headers)
        response = response.json()

        assistant_message = response[0]['generated_text'].split('[/INST]')[-1]
        chat.append({'role': 'assistant', 'content': assistant_message})
        print(f'Assistant: {assistant_message}')

    print(f'Chat: {chat}')
