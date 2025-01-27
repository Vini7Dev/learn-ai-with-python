from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain_openai.chat_models import ChatOpenAI

def execute():
    prompt_template = PromptTemplate.from_template('''
    Qual o melhor nome de empresa para uma empresa que desenvolve o produto: {product_name}.
    Retorne apenas um nome.
    ''')

    chat = ChatOpenAI(model='gpt-3.5-turbo-0125')
    chain = LLMChain(
        llm=chat,
        prompt=prompt_template,
        verbose=True,
    )

    product_name = 'Copos de vidro inquebráveis.'
    response = chain.run(product_name)
    print(f'Resposta: {response}')
