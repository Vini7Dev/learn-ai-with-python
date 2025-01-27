from langchain_community.document_loaders.notion import NotionDirectoryLoader

def execute():
    notion_folder = 'files/notion_db'

    loader = NotionDirectoryLoader(notion_folder)
    document_pages = loader.load()

    print(f'Page 0 Content: {document_pages[0].page_content}')
    print(f'Page 0 Metadata: {document_pages[0].metadata}')
