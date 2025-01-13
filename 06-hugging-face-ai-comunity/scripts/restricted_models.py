import os
import requests

# from transformers import pipeline

def execute():
    # model = pipeline('text-generation', model='google/gemma-7b-it')
    model = 'google/gemma-7b-it'
    url = f'https://api-inference.huggingface.co/models/{model}'
    hugging_face_token = os.getenv('HUGGING_FACE_TOKEN')
    headers = {'Authorization': f'Bearer {hugging_face_token}'}
    json = {
        'options': {'use_cache': False, 'wait_for_model': True},
        'inputs': 'Olá, qual o seu nome?',
    }
    response = requests.post(url, json=json, headers=headers)
    response = response.json()
    print(f'Response: {response}')
