from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chains.conversation.base import ConversationChain
from langchain_openai.chat_models import ChatOpenAI

def execute():
    prompt_template = PromptTemplate.from_template('''
    Essa é uma conversa amigável entre um humano e uma IA.

    Conversa atual:

    {history}
    Human: {input}
    Ai:''')

    chat = ChatOpenAI(model='gpt-3.5-turbo-0125')
    memory = ConversationBufferMemory()
    chain = ConversationChain(
        llm=chat,
        memory=memory,
        prompt=prompt_template,
        verbose=True,
    )

    response = chain.predict(input='Oi')
    print(f'Resposta: {response}')
