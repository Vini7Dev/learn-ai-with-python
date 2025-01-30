from langchain_openai.chat_models import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_text_splitters import RecursiveCharacterTextSplitter

def execute():
    file_paths = [
        'files/Explorando o Universo das IAs com Hugging Face.pdf',
        'files/Explorando a API da OpenAI.pdf',
    ]

    document_pages = []
    for file_path in file_paths:
        loader = PyPDFLoader(file_path)
        document_pages.extend(loader.load())

    recursive_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        separators=['\n\n', '\n', '.', ' ', ''],
    )

    documents = recursive_splitter.split_documents(document_pages)

    for i, document in enumerate(documents):
        document.metadata['source'] = document.metadata['source'].replace('files/', '')
        document.metadata['doc_id'] = i

    chroma_path = 'files/chroma_vector_store_db'
    embeddings_model = OpenAIEmbeddings()
    chroma_vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings_model,
        persist_directory=chroma_path,
    )

    chat = ChatOpenAI(model='gpt-3.5-turbo-0125')

    chat_chain = RetrievalQA.from_chain_type(
        llm=chat,
        retriever=chroma_vector_store.as_retriever(search_type='mmr')
    )

    question = 'O que é Hugging Face e como faço para acessá-lo?'

    response = chat_chain.invoke({ 'query': question })

    print(f'Resposta: {response}')
