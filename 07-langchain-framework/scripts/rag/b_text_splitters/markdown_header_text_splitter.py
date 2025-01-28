import string

from langchain_text_splitters import MarkdownHeaderTextSplitter

def execute():
    headers_to_split_on = [
        ('#', 'Header 1'),
        ('##', 'Header 2'),
        ('###', 'Header 3'),
    ]

    markdown_header_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on,
    )

    markdown_example = '''# Título do Markdown de exemplo
    ## Capítulo 1
    Texto capítulo 1 e mais e mais texto.
    Continuamos no capítulo 1!
    ## Capítulo 2
    Texto capítulo 2 e mais e mais texto.
    Continuamos no capítulo 2!
    ## Capítulo 3
    ### Seção 3.1
    Texto capítulo 3 e mais e mais texto.
    Continuamos no capítulo 3!
    '''

    splits = markdown_header_splitter.split_text(markdown_example)

    print(f'Splits: {splits}')

    for doc in splits:
        print(f'Page content: {doc.page_content}')
        print(f'Metadata: {doc.metadata}')
