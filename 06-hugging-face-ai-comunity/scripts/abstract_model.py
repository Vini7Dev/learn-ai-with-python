import os
import requests

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

def execute():
    hugging_face_token = os.getenv('HUGGING_FACE_TOKEN')
    model = 'csebuetnlp/mT5_multilingual_XLSum'
    url = f'https://api-inference.huggingface.co/models/{model}'

    with open('files/brasil.txt', encoding='utf8') as f:
        file_text = f.read()

    headers = {'Authorization': f'Bearer {hugging_face_token}'}
    json = {
        'inputs': file_text,
        'parameters': {'min_length': 200},
        'options': {'use_cache': False, 'wait_for_model': True},
    }

    response = requests.post(url=url, json=json, headers=headers)
    response = response.json()
    print(f'Response: {response}')
