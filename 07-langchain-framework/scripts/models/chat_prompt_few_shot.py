from langchain_openai.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

def execute():
    messages = [
        HumanMessage(content='Quanto é 1 + 1?'),
        AIMessage(content='2'),
        HumanMessage(content='Quanto é 10 * 5?'),
        AIMessage(content='50'),
        HumanMessage(content='Quanto é 10 + 3?'),
        AIMessage(content='13'),
        HumanMessage(content='Quanto é 5 + 1?'),
    ]
    chat = ChatOpenAI()
    response = chat.invoke(messages)
    print(f'Resposta: {response}')
