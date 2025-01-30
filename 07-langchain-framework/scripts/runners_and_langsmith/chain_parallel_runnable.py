from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

def execute():
    # Run in parallel and combine results

    model = ChatOpenAI()

    output_parser = StrOutputParser()

    prompt_product = ChatPromptTemplate.from_template('Crie um nome para o seguinte produto: {product}')

    chain_product = prompt_product | model | output_parser

    prompt_customers = ChatPromptTemplate.from_template('Descreva o cliente potencial para o seguinte produto: {product}')

    chain_customers = prompt_customers | model | output_parser

    prompt_final = ChatPromptTemplate.from_template('''
    Dado o produto com o seguinte nome e seguinte público potencial, desenvolva um anúncio para o produto.

    Nome do produto: {product_name}
    Público: {customers}''')

    parallel_chain = RunnableParallel({
        'product_name': chain_product,
        'customers': chain_customers,
    })

    chain = parallel_chain | prompt_final | model | output_parser

    response = chain.invoke({ 'product': 'Um como inquebrável' })

    print(f'Resposta: {response}')
