from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai.chat_models import ChatOpenAI

conversations_store = {}

def get_by_session_id(session_id):
    if session_id not in conversations_store:
        conversations_store[session_id] = InMemoryChatMessageHistory()
    return conversations_store[session_id]

def execute():
    prompt = ChatPromptTemplate.from_messages([
        ('system', 'Você é um tutor de programação chamado Asimo. Responda as perguntas de forma didática.'),
        ('placeholder', '{history}'),
        ('human', '{question}'),
    ])

    chain = prompt | ChatOpenAI()

    chain_with_memory = RunnableWithMessageHistory(
        chain,
        get_by_session_id,
        input_messages_key='question',
        history_messages_key='history',
    )

    config = {'configurable': {'session_id': 'user_a'}}

    response = chain_with_memory.invoke({'question': 'O meu nome é Vinícius.'}, config=config)

    print(f'Resposta 1: {response}')

    response = chain_with_memory.invoke({'question': 'Qual é o meu nome?'}, config=config)

    print(f'Resposta 2: {response}')
