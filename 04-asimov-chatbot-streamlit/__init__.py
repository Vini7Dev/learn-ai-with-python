import re
import pickle
from pathlib import Path

import openai
import streamlit as st
from unidecode import unidecode

MESSAGES_FOLDER = Path(__file__).parent / 'messages'
MESSAGES_FOLDER.mkdir(exist_ok=True)

openai_key = 'API_KEY_HERE'

def get_response_stream(messages, api_key, model='gpt-3.5-turbo', temperature=0):
    openai.api_key = api_key
    response_stream = openai.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=messages,
        stream=True,
    )
    return response_stream

def convert_file_name(file_name):
    return re.sub('\W+', '', unidecode(file_name)).lower()

def get_message_name(messages):
    for message in messages:
        if (message['role'] == 'user'):
            return message['content'][:30]

def save_messages(messages):
    if len(messages) == 0:
        return False

    messaage_name = get_message_name(messages=messages)
    file_name = convert_file_name(messaage_name)
    file_to_save = {
        'message_name': messaage_name,
        'file_name': file_name,
        'messages': messages,
    }
    with open(MESSAGES_FOLDER / file_name, 'wb') as f:
        pickle.dump(file_to_save, f)

def load_messages(messages, key='message'):
    if len(messages) == 0:
        return False

    messaage_name = get_message_name(messages=messages)
    file_name = convert_file_name(messaage_name)
    with open(MESSAGES_FOLDER / file_name, 'rb') as f:
        messages = pickle.load(f)
    return messages[key]

def main_page():
    if not 'messages' in st.session_state:
        st.session_state.messages = []

    messages = load_messages(st.session_state.messages)

    st.header('Asimov Chatbot', divider=True)

    for message in messages:
        chat = st.chat_message(message['role'])
        chat.markdown(message['content'])

    prompt = st.chat_input('Fale com o chat')
    if prompt:
        new_message = { 'role': 'user', 'content': prompt }
        chat = st.chat_message(new_message['role'])
        chat.markdown(new_message['content'])
        messages.append(new_message)

    if len(messages) > 0:
        chat = st.chat_message('assistant')
        placeholder = chat.empty()
        placeholder.markdown('▌')
        full_response = ''
        response_stream = get_response_stream(messages=messages, api_key=openai_key)
        for response in response_stream:
            full_response += response.choices[0].delta.content or ''
            placeholder.markdown(f'{full_response}▌')
        placeholder.markdown(f'{full_response}')
        new_message = { 'role': 'assistant', 'content': full_response }
        messages.append(new_message)

    st.session_state.messages = messages
    save_messages(messages=messages)

main_page()
