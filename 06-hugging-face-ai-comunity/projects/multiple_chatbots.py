import os
import requests

import streamlit as st
from transformers import AutoTokenizer
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

hugging_face_token = os.getenv('HUGGING_FACE_TOKEN')

models = {
    'mistralai/Mixtral-8x7B-Instruct-v0.1': '[/INST]',
    'google/gemma-7b-it': '<start_of_turn>model\n',
}

def initialization():
    if 'current_model' not in st.session_state:
        st.session_state['current_model'] = ''
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

def get_model_response(user_message: str, current_model: str, messages):
    if user_message == 'Q':
        return

    messages.append({'role': 'user', 'content': user_message})
    tokenizer = AutoTokenizer.from_pretrained(current_model)
    chat_template = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    url = f'https://api-inference.huggingface.co/models/{current_model}'
    headers = {'Authorization': f'Bearer {hugging_face_token}'}
    json = {
        'options': {'use_cache': False, 'wait_for_model': True},
        'parameters': {'max_new_tokens': 100},
        'inputs': chat_template,
    }
    response = requests.post(url, json=json, headers=headers)
    response = response.json()

    token_model = models[current_model]
    assistant_message = response[0]['generated_text'].split(token_model)[-1]
    messages.append({'role': 'assistant', 'content': assistant_message})
    st.session_state['messages'] = messages
    return assistant_message

def execute():
    initialization()

    current_model = st.selectbox('Selecione um modelo:', options=models)

    if current_model:
        st.session_state['current_model'] = current_model

    chat_area = st.empty()
    user_message = st.chat_input('Faça a sua pergunta aqui: ')

    current_model = st.session_state['current_model']
    messages = st.session_state['messages']

    if user_message:
        get_model_response(
            user_message=user_message,
            current_model=current_model,
            messages=messages,
        )

    with chat_area.container():
        for message in messages:
            chat = st.chat_message(message['role'])
            chat.markdown(message['content'])
