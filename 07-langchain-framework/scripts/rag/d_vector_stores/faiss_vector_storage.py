from langchain_community.vectorstores.faiss import FAISS
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings

def execute(action = 'GET'):
    store_directory = 'files/faiss_vector_store'

    embeddings_model = OpenAIEmbeddings(model='text-embedding-ada-002')

    if action == 'CREATE':
        document_path = 'files/Explorando o Universo das IAs com Hugging Face.pdf'
        loader = PyPDFLoader(document_path)
        documents = loader.load()

        chunk_size = 500    # Make tests
        chunk_overlap = 50  # 10% of "chunk size"
        char_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            # Priority separators order
            separators=['\n\n', '\n', '.', ' ', ''],
        )
        document_splits = char_splitter.split_documents(documents)

        vector_store = FAISS.from_documents(
            embedding=embeddings_model,
            documents=document_splits,
        )

        vector_store.save_local(store_directory)
    else:
        vector_store = FAISS.load_local(
            store_directory,
            embeddings=embeddings_model,
            allow_dangerous_deserialization=True,
        )

        question = 'O que é o Hugging Face?'
        # Getting 5 documents
        simillar_documents = vector_store.similarity_search(question, k=5)
        for doc in simillar_documents:
            print(f'Document Content: {doc.page_content}\n')
            print(f'Document Metadata: {doc.metadata}\n\n')
