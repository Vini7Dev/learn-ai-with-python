import requests
import datetime

from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_openai.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.agents import tool
from pydantic import BaseModel, Field

class TemperatureArgs(BaseModel):
    latitude: float = Field(description='Latitude da localidade que buscamos a temperatura')
    longitude: float = Field(description='Longitude da localidade que buscamos a temperatura')

@tool(args_schema=TemperatureArgs)
def get_current_temperature(latitude: float, longitude: float):
    '''Retorna a temperatura atual para uma dada coordenada'''

    URL = 'https://api.open-meteo.com/v1/forecast'

    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'temperature_2m',
        'forecast_days': 1,
    }

    response = requests.get(URL, params=params)
    if response.status_code == 200:
        result = response.json()

        current_hour = datetime.datetime.now(datetime.UTC).replace(tzinfo=None)
        hour_list = [datetime.datetime.fromisoformat(temp_str) for temp_str in result['hourly']['time']]
        next_index = min(range(len(hour_list)), key=lambda x: abs(hour_list[x] - current_hour))

        current_temperature = result['hourly']['temperature_2m'][next_index]
        return current_temperature
    else:
        raise Exception(f'Request para API {URL} falhou: {response.status_code}')

def execute():
    prompt = ChatPromptTemplate.from_messages([
        ('system', 'Você é um assistente amigável chamado Vinícius.'),
        ('user', '{input}'),
    ])

    chat = ChatOpenAI(model='gpt-3.5-turbo-0125')

    tools = [convert_to_openai_function(get_current_temperature)]

    chain = prompt | chat.bind(functions=tools)

    result = chain.invoke({ 'input': 'Qual é a temperatura de Franca SP?' })

    print(f'Resultado: {result}')
