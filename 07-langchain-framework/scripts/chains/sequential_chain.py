from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.chains.sequential import SequentialChain
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
        output_key='enterprise_name',
        verbose=True,
    )

    prompt_enterprise_description = PromptTemplate.from_template('''
    Dado a empresa com o nome {enterprise_name}
    e que produz o seguinte produto: {product_name}.
    Dê uma descrição de até 50 palavras das atividades dessa empresa.
    ''')

    chain_enterprise_description = LLMChain(
        llm=chat,
        prompt=prompt_enterprise_description,
        output_key='enterprise_description',
        verbose=True,
    )

    prompt_enterprise_translation = PromptTemplate.from_template('''
    Crie um nome em ingles para a empresa chamada {enterprise_name}
    e que tem a seguinte descrição: {enterprise_description}.
    ''')

    chain_enterprise_translation = LLMChain(
        llm=chat,
        prompt=prompt_enterprise_translation,
        output_key='enterprise_english_name',
        verbose=True,
    )

    chain_main = SequentialChain(
        chains=[chain_enterprise_name, chain_enterprise_description, chain_enterprise_translation],
        input_variables=['product_name'],
        output_variables=['enterprise_name', 'enterprise_description', 'enterprise_english_name'],
        verbose=True,
    )

    product_name = 'Copos de vidro inquebráveis.'
    result = chain_main.invoke({ 'product_name': product_name })
    print(f'Resultado: {result}')
    print(f'Nome do Produto: {result['product_name']}')
    print(f'Nome da Empresa: {result['enterprise_name']}')
    print(f'Nome da Empresa em Inglês: {result['enterprise_english_name']}')
    print(f'Descrição da Empresa: {result['enterprise_description']}')
