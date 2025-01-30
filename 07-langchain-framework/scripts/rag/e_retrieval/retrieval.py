from langchain_community.vectorstores.chroma import Chroma
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings

def execute(action = 'SEARCH'):
    store_directory = 'files/retrieval_chroma_vector_store'

    embeddings_model = OpenAIEmbeddings(model='text-embedding-ada-002')

    if action == 'CREATE':
        pdf_files = [
            'files/Explorando o Universo das IAs com Hugging Face.pdf',
            'files/Explorando a API da OpenAI.pdf',
            'files/Explorando a API da OpenAI.pdf',
        ]

        document_pages = []

        for pdf_dir in pdf_files:
            loader = PyPDFLoader(pdf_dir)
            document_pages.extend(loader.load())

        chunk_size = 500    # Make tests
        chunk_overlap = 50  # 10% of "chunk size"
        char_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            # Priority separators order
            separators=['\n\n', '\n', '.', ' ', ''],
        )
        document_splits = char_splitter.split_documents(document_pages)

        for i, document in enumerate(document_splits):
            document.metadata['source'] = document.metadata['source'].replace('files/', '')
            document.metadata['doc_id'] = i

        created_vector_store = Chroma.from_documents(
            persist_directory=store_directory,
            embedding=embeddings_model,
            documents=document_splits,
        )

        print(f'Total of documents: {created_vector_store._collection.count()}')
    else:
        vector_store = Chroma(
            embedding_function=embeddings_model,
            persist_directory=store_directory,
        )

        '''
        question = 'O que é a OpenAI?'

        semantic_documents = vector_store.similarity_search(question, k=3)

        print(f'Question: {question}')
        for document in semantic_documents:
            print(f'Simillar: {document.page_content}')
            print(f'Metadata: {document.metadata}\n\n')
        '''

        question = 'O que é a OpenAI?'

        # Avoid very simmilar texts
        mmr_documents = vector_store.max_marginal_relevance_search(question, k=3, fetch_k=10)

        print(f'Question: {question}')
        for document in mmr_documents:
            print(f'MMR: {document.page_content}')
            print(f'Metadata: {document.metadata}\n\n')

        '''
        question = 'O que a apostila de Hugging Face fala sobre a OpenAI e o ChatGPT?'

        # Using filters
        semantic_documents = vector_store.similarity_search(
            question,
            k=3,
            filter={
                '$and': [
                    {'source': {'$in': ['Explorando o Universo das IAs com Hugging Face.pdf']}},
                    {'page': {'$in': [10, 11, 12, 13]}},
                ],
            },
        )

        print(f'Question: {question}')
        for document in semantic_documents:
            print(f'Simillar: {document.page_content}')
            print(f'Metadata: {document.metadata}\n\n')
        '''
