from langchain_openai.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

def execute():
    prompt = ChatPromptTemplate.from_template('Fale uma curiosidade sobre o assunto: {subject}')
    chain_subject = prompt | ChatOpenAI() | StrOutputParser()

    prompt = ChatPromptTemplate.from_template('Crie uma história sobre o seguinte fato curioso: {subject}')
    chain_curious = prompt | ChatOpenAI() | StrOutputParser()

    chain_main = chain_subject | chain_curious

    response = chain_main.invoke({ 'subject': 'gatinhos' })

    print(f'Response: {response}')
