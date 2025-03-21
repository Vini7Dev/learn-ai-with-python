from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def execute():
    prompt = ChatPromptTemplate.from_template('Crie uma frase sobre o seguinte assunto: {subject}')

    print(f'Prompt: {prompt.input_schema.model_json_schema()}')

    model = ChatOpenAI(model='gpt-3.5-turbo-0125')

    # print(f'Model: {model.input_schema.model_json_schema()}')

    output_parser = StrOutputParser()

    # print(f'Output Parser: {output_parser.input_schema.model_json_schema()}')

    chain = prompt | model | output_parser

    response = chain.invoke({'subject': 'Ggatinhos'})

    print(f'Resposta: {response}')
