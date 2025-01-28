from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def execute():
    chunk_size = 100    # Make tests
    chunk_overlap = 10  # 10% of "chunk size"

    char_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        # Priority separators order
        separators=['\n\n', '\n', ' ', ''],
    )

    document_path = 'files/Explorando o Universo das IAs com Hugging Face.pdf'

    loader = PyPDFLoader(document_path)

    documents = loader.load()

    splits = char_splitter.split_documents(documents)

    print(f'Splits: {splits}')
    print(f'Total of Splits: {len(splits)}')
