from langchain_openai.chat_models import ChatOpenAI
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class UnityEnum(str, Enum):
    celscius = 'celsius'
    fahrenheit = 'fahrenheit'

class GetCurrentTemperature(BaseModel):
    """Obtém a temperatura atual em cada cidade"""
    city: str = Field(description='O nome da cidade', examples=['São Paulo', 'Porto Alegre'])
    unity: Optional[UnityEnum]

def execute():
    temperature_tool = convert_to_openai_function(GetCurrentTemperature)

    prompt = ChatPromptTemplate.from_messages([
        ('system', 'Você é um assistente amigável chamado Isaac'),
        ('user', '{input}')
    ])

    chat = ChatOpenAI()

    '''
    response = chat.invoke(
        'Qual é a temperatura de Porto Alegre?',
        functions=[temperature_tool],
        function_call={'name': 'GetCurrentTemperature'},
    )
    '''

    chain = prompt | chat.bind(functions=[temperature_tool])

    response = chain.invoke({'input': 'Olá'})

    print(f'Resposta: {response}')

    response = chain.invoke({'input': 'Qual a temperatura em Floripa?'})

    print(f'Resposta: {response}')
