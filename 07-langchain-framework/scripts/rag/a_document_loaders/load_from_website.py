from langchain_community.document_loaders.web_base import WebBaseLoader

def execute():
    site_url = 'https://hub.asimov.academy/blog/listas-em-python/'

    loader = WebBaseLoader(site_url)
    documents = loader.load()

    print(f'Document url 0 Content: {documents[0].page_content}')
    print(f'Document url 0 Metadata: {documents[0].metadata}')
