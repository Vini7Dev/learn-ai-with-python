from langchain_openai.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.utils.function_calling import convert_to_openai_function
from pydantic import BaseModel, Field
from typing import List

class Recipe(BaseModel):
    '''Informações de utensílios e ingredientes necessários para uma receita'''
    utensils: List[str] = Field(description='Lista de utencílios de cozinha necessários para a receita.')
    ingredients: List[str] = Field(description='Lista de Ingredientes necessários para fazer a receita.')

def execute():
    recipe = '''
    Massa:
    1. Em um liquidificador, adicione a cenoura, os ovos e o óleo, depois misture.
    2. Acrescente o açúcar e bata novamente por 5 minutos.
    3. Em uma tigela ou na batedeira, adicione a farinha de trigo e depois misture novamente.
    4. Acrescente o fermento e misture lentamente com uma colher.
    5. Asse em um forno preaquecido a 180° C por aproximadamente 40 minutos.

    Cobertura:
    6. Despeje em uma tigela a manteiga, o chocolate em pó, o açúcar e o leite, depois misture.
    7. Leve a mistura ao fogo e continue misturando até obter uma consistência cremosa, depois despeje a calda por cima do bolo.
    '''

    tool_recipe = convert_to_openai_function(Recipe)
    print(f'===> Tool: {tool_recipe}')

    prompt = ChatPromptTemplate.from_messages([
        ('system', 'Você deve extrair os utensílios de cozinha e os ingredientes necessários para fazer a receita que te for informada.'),
        ('user', '{input}'),
    ])

    chat = ChatOpenAI()

    chain = (prompt
              | chat.bind(functions=[tool_recipe], function_call={'name': 'Recipe'})
              | JsonOutputFunctionsParser())

    result = chain.invoke({'input': recipe})

    print(f'Resultado: {result}')
