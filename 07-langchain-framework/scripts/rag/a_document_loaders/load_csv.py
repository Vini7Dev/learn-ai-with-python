from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.chains.question_answering import load_qa_chain
from langchain_openai.chat_models import ChatOpenAI

def execute():
    csv_file_path = 'files/Top 1000 IMDB movies.csv'

    loader = CSVLoader(csv_file_path)
    document_rows = loader.load()

    # print(f' Row 0 Content: {document_rows[0].page_content}')
    # print(f' Row 0 Metadata: {document_rows[0].metadata}')
    # print(f' Row 1 Content: {document_rows[1].page_content}')
    # print(f' Row 1 Metadata: {document_rows[1].metadata}')

    chat = ChatOpenAI(model='gpt-3.5-turbo-0125')
    chain = load_qa_chain(llm=chat, chain_type='stuff', verbose=True)

    question = 'Qual é o filme com maior metascore?'
    response = chain.run(input_documents=document_rows[:10], question=question)
    print(f'Resposta: {response}')
