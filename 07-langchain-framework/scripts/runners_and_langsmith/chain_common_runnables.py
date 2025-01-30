from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

def execute():
    model = ChatOpenAI()
    output_parser = StrOutputParser()

    prompt = ChatPromptTemplate.from_template('Fale uma curiosidade sobre o assunto: {subject}')

    chain = prompt | model | output_parser

    # COMMON RUNNABLES

    '''
    chain.invoke({ 'subject': '<Query-Text-Here>' })
    chain.invoke('<Query-Text-Here>') # When has only one param
    '''

    '''
    for chunk in chain.stream('<Query-Text-Here>'):
        print(chunk.content, end='')
    '''

    '''
    ## Run in parallel
    chain.batch([
        { 'subject': '<Query-1-Text-Here>' },
        { 'subject': '<Query-2-Text-Here>' },
        { 'subject': '<Query-3-Text-Here>' },
        { 'subject': '<Query-4-Text-Here>' },
    ])

    chain.batch([
        { 'subject': '<Query-1-Text-Here>' },
        { 'subject': '<Query-2-Text-Here>' },
        { 'subject': '<Query-3-Text-Here>' },
        { 'subject': '<Query-4-Text-Here>' },
    ], config={'max_concurrency': 2})
    '''
