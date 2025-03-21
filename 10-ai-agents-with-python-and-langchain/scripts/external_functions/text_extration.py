from langchain_openai.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.utils.function_calling import convert_to_openai_function
from pydantic import BaseModel, Field
from typing import List

class Occurrence(BaseModel):
    '''Informação sobre um acontecimento'''
    date: str = Field(description='Data do acontecimento no formato YYYY-MM-DD')
    description: str = Field(description='Acontecimento extraído do texto')

class OccurrenceList(BaseModel):
    '''Acontecimentos para exibição'''
    occurrences: List[Occurrence] = Field(description='Lista de acontecimentos presentes no texto informal')

def execute():
    text = '''A Apple foi fundada em 1 de abril de 1976 por Steve Wozniak, Steve Jobs e Ronald Wayne
    com o nome de Apple Computers, na Califórnia. O nome foi escolhido por Jobs após a visita do pomar
    de maçãs da fazenda de Robert Friedland, também pelo fato do nome soar bem e ficar antes da Atari
    nas listas telefônicas.

    O primeiro protótipo da empresa foi o Apple I que foi demonstrado na Homebrew Computer Club em 1975,
    as vendas começaram em julho de 1976 com o preço de US$ 666,66, aproximadamente 200 unidades foram
    vendidas,[21] em 1977 a empresa conseguiu o aporte de Mike Markkula e um empréstimo do Bank of America.'''

    tool_occurrence_list = convert_to_openai_function(OccurrenceList)

    prompt = ChatPromptTemplate.from_messages([
        ('system', 'Extraia as frases de acontecimentos. Elas devem ser extraídas integralmente.'),
        ('user', '{input}')
    ])

    chat = ChatOpenAI()

    chain = (prompt
             | chat.bind(functions=[tool_occurrence_list], function_call={'name': 'OccurrenceList'})
             | JsonOutputFunctionsParser())

    result = chain.invoke({'input': text})

    print(f'Resultado: {result}')
