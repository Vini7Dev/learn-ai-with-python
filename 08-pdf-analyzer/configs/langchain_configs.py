import streamlit as st

LLM_MODEL_NAME = 'gpt-3.5-turbo-0125'
RETRIEVAL_SEARCH_TYPE = 'mmr'
RETRIEVAL_KWARGS = '{"k": 5, "fetch_k": 20}'
RETRIEVAL_PROMPT = '''Você é um Chatbot amigável que auxilia na interpretação
de documentos que lhe são fornecidos.
No contexto forncido estão as informações dos documentos do usuário.
Utilize o contexto para responder as perguntas do usuário.
Se você não sabe a resposta, apenas diga que não sabe e não tente
inventar a resposta.

Contexto:
{context}

Conversa atual:
{chat_history}
Human: {question}
AI: '''

default_config = {
    'llm_model_name': LLM_MODEL_NAME,
    'retrieval_search_type': RETRIEVAL_SEARCH_TYPE,
    'retrieval_kwargs': RETRIEVAL_KWARGS,
    'retrieval_prompt': RETRIEVAL_PROMPT,
}

def get_langchain_config(config_name):
    if config_name.lower() in st.session_state:
        return st.session_state[config_name]

    return default_config[config_name]

def update_langchain_configs(configs):
    for config_name in configs:
        st.session_state[config_name] = configs[config_name]
