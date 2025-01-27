from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.chains.sequential import SimpleSequentialChain
from langchain_openai.chat_models import ChatOpenAI

def execute():
    chat = ChatOpenAI(model='gpt-3.5-turbo-0125')

    prompt_enterprise_name = PromptTemplate.from_template('''
    Qual o melhor nome de empres para uma empresa que desenvolve o produto: {product_name}.
    Retorne apenas um nome.
    ''')

    chain_enterprise_name = LLMChain(
        llm=chat,
        prompt=prompt_enterprise_name,
        verbose=True,
    )

    prompt_enterprise_description = PromptTemplate.from_template('''
    Dado a empresa com o seguinte nome: {enterprise_name}.
    Dê uma descrição de até 50 palavras das atividades dessa empresa.
    ''')

    chain_enterprise_description = LLMChain(
        llm=chat,
        prompt=prompt_enterprise_description,
        verbose=True,
    )

    chain_main = SimpleSequentialChain(
        chains=[chain_enterprise_name, chain_enterprise_description],
        verbose=True,
    )

    product_name = 'Copos de vidro inquebráveis.'
    result = chain_main.run(product_name)
    print(f'Resultado: {result}')
