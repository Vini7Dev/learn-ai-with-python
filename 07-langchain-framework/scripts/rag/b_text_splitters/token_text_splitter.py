import string

from langchain_text_splitters import TokenTextSplitter

def execute():
    chunk_size = 50    # Make tests
    chunk_overlap = 5  # 10% of "chunk size"

    token_splitter = TokenTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    text = ''.join(f'{string.ascii_lowercase}' for _ in range(5))

    splits = token_splitter.split_text(text)

    print(f'Splits: {splits}')
