from langchain.memory import ConversationSummaryBufferMemory
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
    # Create a System message with the SUMMARY of conversation. To save some contexts
    memory = ConversationSummaryBufferMemory(llm=chat, max_token_limit=250)
    conversation = ConversationChain(
        llm=chat,
        memory=memory,
        verbose=True,
    )

    response = conversation.predict(input='Olá! O meu nome é Vinícius.')
    print(f'Resposta: {response}')

    response = conversation.predict(input='Me conte uma história de 500 palavras.')
    print(f'Resposta: {response}')

    response = conversation.predict(input='Qual é o meu nome?')
    print(f'Resposta: {response}')
