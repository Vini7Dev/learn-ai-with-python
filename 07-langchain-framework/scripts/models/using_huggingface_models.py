from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_models import ChatHuggingFace
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint

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
    model = 'mistralai/Mixtral-8x7B-Instruct-v0.1'
    llm = HuggingFaceEndpoint(repo_id=model)
    chat = ChatHuggingFace(llm=llm)
    response = chat.invoke(messages)
    print(f'Resposta: {response}')
