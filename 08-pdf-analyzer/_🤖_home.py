import time

import streamlit as st
from langchain.memory import ConversationBufferMemory

from services.langchain import PDFS_FOLDER
from services.langchain import initialize_chat

def sidebar():
    uploaded_pdfs = st.file_uploader(
        'Adicione seus arquivos PDFs',
        type=['.pdf'],
        accept_multiple_files=True,
    )

    if not uploaded_pdfs is None:
        for file in PDFS_FOLDER.glob('*.pdf'):
            file.unlink()
        for pdf in uploaded_pdfs:
            with open(PDFS_FOLDER / pdf.name, 'wb') as f:
                f.write(pdf.read())

    button_label = 'Inicializar Chat'
    if 'chain' in st.session_state:
        button_label = 'Atualizar Chat'
    if st.button(button_label, use_container_width=True):
        initialize_chat()

def chat_window():
    st.header('🤖 Bem-vindo ao Chat PDF', divider=True)

    if not 'chain' in st.session_state:
        st.error('Faça o upload de PDFs para começar!')
        st.stop()

    chain = st.session_state['chain']
    memory = chain.memory
    messages = memory.load_memory_variables({})['chat_history']

    container = st.container()
    for message in messages:
        chat = container.chat_message(message.type)
        chat.markdown(message.content)

    new_message = st.chat_input('Converse com os seus documentos...')
    if not new_message is None:
        chat = container.chat_message('human')
        chat.markdown(new_message)

        chat = container.chat_message('ai')
        chat.markdown('Gerando resposta...')
        response = chain.invoke({ 'question': new_message })
        st.session_state['last_response'] = response

        st.rerun()

def main():
    with st.sidebar:
        sidebar()

    chat_window()


if __name__ == '__main__':
    main()
