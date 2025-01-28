from langchain_text_splitters import RecursiveCharacterTextSplitter

def execute():
    chunk_size = 100    # Make tests
    chunk_overlap = 10  # 10% of "chunk size"

    char_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        # Priority separators order
        separators=['\n\n', '\n', '.', ' ', ''],
    )

    text = '''
    Já conhece a lista em Python? Quer entender como manipular listas e quais são suas principais utilidades e métodos? Sabe qual a diferença entre listas e tuplas? Este artigo responde responde isso e muito mais! Aproveite ao máximo todo o potencial dessa estrutura de dados essencial para a programação em Python.

    A lista em Python é uma das estruturas de dados fundamentais da linguagem Python. Além de possuir grande versatilidade, as listas são extremamente relevantes para iniciantes na programação, por incorporar uma variedade de conceitos básicos de Python como mutabilidade, indexação, iteração e slicing. Mas você já conhece as listas de Python a fundo?

    Neste artigo, vamos nos aprofundar nas listas em Python e aprender a utilizá-las em seus códigos. Ao longo do texto, você aprenderá como criar e manipular uma lista em Python, quais os principais métodos de listas, e como elas se relacionam e com outros tipos de dados de Python, como strings, tuplas e vetores. Vamos lá!

    '''

    splits = char_splitter.split_text(text)

    print(f'Splits: {splits}')
