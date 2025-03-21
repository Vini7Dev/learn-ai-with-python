from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_openai.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

class Feeling(BaseModel):
    """Define o sentimento e a língua da mensagem"""
    feeling: str = Field(description='Sentimento do texto. Deve ser "pos", "neg" ou "nd" para não definido.')
    language: str = Field(description='Língua que o texto foi escrito. Deve estar no formato ISO 639-1.')

def execute():
    prompt = ChatPromptTemplate.from_messages([
        ('system', 'Pense com cuidado ao categorizr o texto conforme as instruções.'),
        ('user', '{input}')
    ])

    chat = ChatOpenAI()

    tool_feeling = convert_to_openai_function(Feeling)

    chain = (prompt
        | chat.bind(functions=[tool_feeling], function_call={'name': 'Feeling'})
        | JsonOutputFunctionsParser())

    text = 'Eu gosto muito de massa aos quatro queijos'

    result = chain.invoke({'input': text})

    print(f'Resultado: {result}')
