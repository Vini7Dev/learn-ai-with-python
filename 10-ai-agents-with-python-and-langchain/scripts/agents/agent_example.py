import requests
import datetime

from pydantic import BaseModel, Field
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain.agents import tool
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.agent import AgentFinish

import wikipedia
wikipedia.set_lang('pt')

class GetTemperatureArgs(BaseModel):
    latitude: float = Field(description='Latitude da localidade que buscamos a temperatura')
    longitude: float = Field(description='Longitude da localidade que buscamos a temperatura')

@tool(args_schema=GetTemperatureArgs)
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
        next_hour_index = min(range(len(hour_list)), key=lambda x: abs(hour_list[x] - current_hour))

        current_temperature = result['hourly']['temperature_2m'][next_hour_index]
        return f'{current_temperature}ºC'
    else:
        raise Exception(f'Request para API {URL} falhou: {response.status_code}')

@tool
def wikipedia_search(query: str):
    """Faz busca no wikipedia e retorna resumos de páginas para a query"""
    page_titles = wikipedia.search(query)
    abstracts = []
    for title in page_titles[:3]:
        try:
            wiki_page = wikipedia.page(title=title, auto_suggest=True)
            abstracts.append(f'Título da página: {title}\nResumo: {wiki_page.summary}')
        except:
            pass
    if not abstracts:
        return 'Busca não teve retorno'
    else:
        return '\n\n'.join(abstracts)

def run_agent(tool_run, chain, inputData):
    intermediate_steps = []
    while True:
        response = chain.invoke({'input': inputData, 'intermediate_steps': intermediate_steps})
        if (isinstance(response, AgentFinish)):
            return response
        observation = tool_run[response.tool].run(response.tool_input)
        intermediate_steps.append((response, observation))

def execute():
    prompt = ChatPromptTemplate.from_messages([
        ('system', 'Você é um assistente amigável chamado Isaac'),
        ('user', '{input}'),
        MessagesPlaceholder(variable_name='agent_scratchpad')
    ])

    chat = ChatOpenAI()

    tools = [wikipedia_search, get_current_temperature]
    tools_json = [convert_to_openai_function(tool) for tool in tools]
    tool_run = {tool.name: tool for tool in tools}

    pass_through = RunnablePassthrough.assign(
        agent_scratchpad = lambda x: format_to_openai_function_messages(x['intermediate_steps'])
    )

    chain = pass_through | prompt | chat.bind(functions=tools_json) | OpenAIFunctionsAgentOutputParser()

    result = run_agent(
        tool_run=tool_run,
        chain=chain,
        inputData='Qual é a temperatura em Franca SP?',
    )

    print(f'Resultado: {result}')
