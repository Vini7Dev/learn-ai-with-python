import re
import pickle
from pathlib import Path

import openai
import streamlit as st
from unidecode import unidecode

CONFIGS_FOLDER = Path(__file__).parent / 'configs'
CONFIGS_FOLDER.mkdir(exist_ok=True)
MESSAGES_FOLDER = Path(__file__).parent / 'messages'
MESSAGES_FOLDER.mkdir(exist_ok=True)
CACHE_MESSAGE_NAMES = {}

def save_api_key(api_key):
    with open(CONFIGS_FOLDER / 'api_key', 'wb') as f:
        pickle.dump(api_key, f)

def read_api_key():
    if (CONFIGS_FOLDER / 'api_key').exists():
        with open(CONFIGS_FOLDER / 'api_key', 'rb') as f:
            return pickle.load(f)
    else:
        return ''

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

def unconvert_file_name(file_name):
    if file_name not in CACHE_MESSAGE_NAMES:
        message_name = load_messages_name_by_file(file_name, key='message_name')
        CACHE_MESSAGE_NAMES[file_name] = message_name
        return message_name
    return CACHE_MESSAGE_NAMES[file_name]

def get_message_name(messages):
    print('===> messages', messages)

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

def load_messages(messages, key='messages'):
    if len(messages) == 0:
        return []

    messaage_name = get_message_name(messages=messages)
    file_name = convert_file_name(messaage_name)
    with open(MESSAGES_FOLDER / file_name, 'rb') as f:
        messages = pickle.load(f)
    return messages[key]

def load_messages_name_by_file(file_name, key='messages'):
    with open(MESSAGES_FOLDER / file_name, 'rb') as f:
        messages = pickle.load(f)
    return messages[key]

def inicialization():
    if not 'messages' in st.session_state:
        st.session_state.messages = []
    if not 'current_chat' in st.session_state:
        st.session_state.current_chat = ''
    if not 'openai_model' in st.session_state:
        st.session_state.openai_model = 'gpt-3.5-turbo'
    if not 'openai_key' in st.session_state:
        st.session_state.openai_key = read_api_key()

def main_page():
    messages = load_messages(st.session_state.messages)

    st.header('Asimov Chatbot', divider=True)

    for message in messages:
        chat = st.chat_message(message['role'])
        chat.markdown(message['content'])

    prompt = st.chat_input('Fale com o chat')
    if prompt:
        if st.session_state.openai_key == '':
            st.error('Adicione uma API Key na aba de configurações')
            return

        new_message = { 'role': 'user', 'content': prompt }
        chat = st.chat_message(new_message['role'])
        chat.markdown(new_message['content'])
        messages.append(new_message)

        chat = st.chat_message('assistant')
        placeholder = chat.empty()
        placeholder.markdown('▌')
        full_response = ''
        response_stream = get_response_stream(
            messages=messages,
            api_key=st.session_state.openai_key,
            model=st.session_state.openai_model,
        )
        for response in response_stream:
            full_response += response.choices[0].delta.content or ''
            placeholder.markdown(f'{full_response}▌')
        placeholder.markdown(f'{full_response}')
        new_message = { 'role': 'assistant', 'content': full_response }
        messages.append(new_message)

    st.session_state.messages = messages
    save_messages(messages=messages)

def select_chat(file_name):
    if file_name == '':
        st.session_state.messages = []
    else:
        messages = load_messages_name_by_file(file_name)
        st.session_state.messages = messages
    st.session_state.current_chat = file_name

def list_chat_file_names():
    chats = list(MESSAGES_FOLDER.glob('*'))
    chats = sorted(chats, key=lambda item: item.stat().st_mtime_ns, reverse=True)
    return [c.stem for c in chats]

def tab_chats(tab):
    tab.button('+ Nova conversa',
               on_click=select_chat,
               args=('', ),
               use_container_width=True)
    tab.markdown('')
    chat_file_names = list_chat_file_names()
    if len(chat_file_names) >= 30:
        chat_file_names += '...'
    for file_name in chat_file_names:
        message_name = unconvert_file_name(file_name).capitalize()
        tab.button(message_name,
                on_click=select_chat,
                args=(file_name, ),
                disabled=file_name==st.session_state.current_chat,
                use_container_width=True)

def tab_configs(tab):
    openai_model = tab.selectbox('Selecione o modelo', ['gpt-3.5-turbo', 'gpt-4'])
    st.session_state.openai_model = openai_model
    openai_key = tab.text_input('Adicione a sua API Key da OpenAI', st.session_state.openai_key)
    if openai_key != st.session_state.openai_key:
        st.session_state.openai_key = openai_key
        save_api_key(openai_key)
        st.success('Chave salva com sucesso!')

def main():
    inicialization()
    main_page()
    tab1, tab2 = st.sidebar.tabs(['Conversas', 'Configurações'])
    tab_chats(tab1)
    tab_configs(tab2)

if __name__ == '__main__':
    main()
