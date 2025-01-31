import json

import streamlit as st

from utils.get_array_value_index import get_array_value_index
from configs.langchain_configs import get_langchain_config, update_langchain_configs
from services.langchain import initialize_chat

LLM_MODEL_NAMES = ['gpt-3.5-turbo-0125', 'gpt-4o-mini']
RETIEVAL_SEARCH_TYPES = ['mmr']

def config_page():
    st.header('Página de configuração', divider=True)

    llm_model_name_index = get_array_value_index(
        array=LLM_MODEL_NAMES,
        value=get_langchain_config('llm_model_name'),
    )
    retrieval_search_type_index = get_array_value_index(
        array=RETIEVAL_SEARCH_TYPES,
        value=get_langchain_config('retrieval_search_type'),
    )

    input_llm_model_name = st.selectbox(
        'Modifique o modelo',
        options=['gpt-3.5-turbo-0125', 'gpt-4o-mini'],
        index=llm_model_name_index,
    )
    input_retrieval_search_type = st.selectbox(
        'Modifique o tipo de busca',
        options=['mmr'],
        index=retrieval_search_type_index,
    )
    input_retrieval_kwargs = st.text_input(
        'Modifique os argumentos de busca',
        value=json.dumps(get_langchain_config('retrieval_kwargs')),
    )
    input_retrieval_prompt = st.text_area(
        'Modifique o prompt padrção',
        height=350,
        value=get_langchain_config('retrieval_prompt'),
    )

    if st.button('Atualizar', use_container_width=True):
        update_langchain_configs({
            'llm_model_name': input_llm_model_name,
            'retrieval_search_type': input_retrieval_search_type,
            'retrieval_prompt': input_retrieval_prompt,
            'retrieval_kwargs': json.loads(input_retrieval_kwargs),
        })

    if st.button('Recarregar Chat', use_container_width=True):
        initialize_chat()

config_page()
