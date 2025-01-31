import streamlit as st
from langchain.prompts import PromptTemplate

from configs.langchain_configs import get_langchain_config

def debug_page():
    st.header('Página de Depuração', divider=True)

    if not 'last_response' in st.session_state:
        st.error('Realize uma pergunta para o modelo para visualizar a depuração!')
        st.stop()

    prompt_template = get_langchain_config('retrieval_prompt')
    prompt_template = PromptTemplate.from_template(prompt_template)

    last_response = st.session_state['last_response']

    context_docs = last_response['source_documents']
    context_list = [doc.page_content for doc in context_docs]
    context_str = '\n\n'.join(context_list)

    chain = st.session_state['chain']
    memory = chain.memory
    chat_history = memory.buffer_as_str

    with st.container(border=True):
        prompt = prompt_template.format(
            chat_history=chat_history,
            context=context_str,
            question='',
        )
        st.code(prompt)

debug_page()
