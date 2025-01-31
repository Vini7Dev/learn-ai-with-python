import json
from pathlib import Path

import streamlit as st
from dotenv import find_dotenv, load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai.chat_models import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings

from configs.langchain_configs import get_langchain_config

PDFS_FOLDER = Path(__file__).parent / '..' / 'files'
PDFS_FOLDER.mkdir(exist_ok=True)

_ = load_dotenv(find_dotenv())

def import_documents():
    documents = []
    for file in PDFS_FOLDER.glob('*.pdf'):
        loader = PyPDFLoader(str(file))
        documents.extend(loader.load())

    return documents

def split_documents(documents = []):
    chunk_size = 2500
    chunk_overlap = 250
    recursive_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=['\n\n', '\n', '.', ' ', ''],
    )

    documents = recursive_splitter.split_documents(documents)
    for i, document in enumerate(documents):
        document.metadata['source'] = document.metadata['source'].split('/')[-1]
        document.metadata['id'] = i

    return documents

def create_vector_store(documents):
    embedding_model = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(
        embedding=embedding_model,
        documents=documents,
    )
    return vector_store

def create_chain(vector_store):
    chat_llm = ChatOpenAI(model=get_langchain_config('llm_model_name'))
    memory = ConversationBufferMemory(
        return_messages=True,
        memory_key='chat_history',
        output_key='answer',
    )
    retriever = vector_store.as_retriever(
        search_type=get_langchain_config('retrieval_search_type'),
        search_kwargs=json.loads(get_langchain_config('retrieval_kwargs')),
    )
    prompt_template = PromptTemplate.from_template(get_langchain_config('retrieval_prompt'))
    chat_chain = ConversationalRetrievalChain.from_llm(
        llm=chat_llm,
        memory=memory,
        retriever=retriever,
        return_source_documents=True,
        combine_docs_chain_kwargs={'prompt': prompt_template},
        verbose=True,
    )
    return chat_chain

def initialize_chat():
    if len(list(PDFS_FOLDER.glob('*.pdf'))) == 0:
        st.error('Adicione arquivos .pdf para inicializar o Chat!')
        st.stop()

    st.success('Inicializando o Chat...')
    documents = import_documents()
    splited_documents = split_documents(documents=documents)
    vector_store = create_vector_store(documents=splited_documents)
    conversation_chain = create_chain(vector_store)
    st.session_state['chain'] = conversation_chain
    st.rerun()
