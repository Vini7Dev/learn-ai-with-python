from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

def execute():
    messages = [
        SystemMessage(content='Você é um assistente que conta piadas.'),
        HumanMessage(content='Quanto é 1 + 1?'),
    ]

    chat = ChatOpenAI(model='gpt-3.5-turbo-0125')
    print('Resposta: ', end='')
    for part in chat.stream(messages):
        print(part.content, end='')
