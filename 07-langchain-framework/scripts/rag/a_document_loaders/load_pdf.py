from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain.chains.question_answering import load_qa_chain
from langchain_openai.chat_models import ChatOpenAI

def execute():
    pdf_file_path = 'files/Explorando o Universo das IAs com Hugging Face.pdf'

    loader = PyPDFLoader(pdf_file_path)
    document_pages = loader.load()

    # print(f' Page 0 Content: {document_pages[0].page_content}')
    # print(f' Page 0 Metadata: {document_pages[0].metadata}')
    # print(f' Page 1 Content: {document_pages[1].page_content}')
    # print(f' Page 1 Metadata: {document_pages[1].metadata}')

    chat = ChatOpenAI(model='gpt-3.5-turbo-0125')
    chain = load_qa_chain(llm=chat, chain_type='stuff', verbose=True)

    question = 'Quais assuntos são tratados no documento?'
    response = chain.run(input_documents=document_pages[:10], question=question)
    print(f'Resposta: {response}')
