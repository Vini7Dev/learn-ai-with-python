from langchain_openai.chat_models import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter

def execute():
    file_paths = [
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

    faiss_path = 'files/faiss_vector_store_db'
    embeddings_model = OpenAIEmbeddings()
    faiss_vector_store = FAISS.from_documents(
        documents=documents,
        embedding=embeddings_model,
    )
    faiss_vector_store.save_local(faiss_path)

    chat_prompt = ChatPromptTemplate.from_template('''
    Responda as pergutas se baseando no contexto fornecido.

    Contexto: {context}

    Pergunta: {question}
    ''')

    retriever = faiss_vector_store.as_retriever(
        search_type='mmr',
        search_kwargs={'k': 5, 'fetch_k': 25},
    )

    setup = RunnableParallel({
        'question': RunnablePassthrough(),
        'context': retriever,
    })

    input = setup.invoke('O que é a OpenAI?')

    input['context'] = '\n\n'.join([c.page_content for c in input['context']])

    print(f'Contexto: {input['context']}')

    chain = setup | chat_prompt | ChatOpenAI()
    response = chain.invoke('O que é a OpenAI?')

    print(f'Resposta: {response}')
