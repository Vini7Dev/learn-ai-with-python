from langchain.memory import ConversationTokenBufferMemory
from langchain_openai.chat_models import ChatOpenAI
from langchain.chains.conversation.base import ConversationChain

def execute():
    '''
    memory = ConversationBufferMemory(return_messages=True)
    memory.chat_memory.add_user_message('Oi?')
    memory.chat_memory.add_ai_message('Como vai?')
    result = memory.load_memory_variables({})
    print(f'Resultado: {result}')
    '''

    chat = ChatOpenAI()
    # LIMIT TOKENS TO SEND
    memory = ConversationTokenBufferMemory(llm=chat, max_token_limit=250)
    conversation = ConversationChain(
        llm=chat,
        memory=memory,
        verbose=True,
    )

    response = conversation.predict(input='Me conte uma história de 500 palavras.')
    print(f'Resposta: {response}')

    response = conversation.predict(input='Resuma a história anterior.')
    print(f'Resposta: {response}')
