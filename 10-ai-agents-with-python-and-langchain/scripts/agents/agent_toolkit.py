from langchain_openai.chat_models import ChatOpenAI
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.base import create_sql_agent

def execute():
    database = SQLDatabase.from_uri('sqlite:///files/Chinook.db')

    chat = ChatOpenAI(model='gpt-3.5-turbo-0125')

    agent_executor = create_sql_agent(
        chat,
        db=database,
        verbose=True,
        agent_type='tool-calling',
    )

    print('===> Ferramentas <===')
    for tool in agent_executor.tools:
        print(f'Nome: {tool.name}')
        print(f'Descrição: {tool.description}')
        print(f'Argumentos: {tool.args}')
        print('------------------')

    # result = agent_executor.invoke({'input': 'Qual artista possuí mais albuns?'})
    result = agent_executor.invoke({'input': 'Me descreva a base de dados.'})

    print(f'Resultado: {result}')
