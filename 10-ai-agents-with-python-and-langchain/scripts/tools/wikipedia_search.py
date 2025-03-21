from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_core.agents import AgentFinish
from langchain_openai.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.agents import tool

import wikipedia
wikipedia.set_lang('pt')

@tool
def wikipedia_search(query: str):
    """Faz busca no wikipedia e retorna resumos de páginas para a query"""
    page_titles = wikipedia.search(query)
    abstracts = []
    for titulo in page_titles[:3]:
        try:
            wiki_page = wikipedia.page(title=titulo, auto_suggest=True)
            abstracts.append(f'Título da página: {titulo}\nResumo: {wiki_page.summary}')
        except:
            pass
    if not abstracts:
        return 'Busca não teve retorno'
    else:
        return '\n\n'.join(abstracts)

tools = [wikipedia_search]
tools_json = [convert_to_openai_function(tool) for tool in tools]
tool_run = { tool.name: tool for tool in tools }
# tool_run['wikipedia_search'].invoke({ 'query': 'Brasil' })

def routing(result):
    if isinstance(result, AgentFinish):
        return result.return_values['output']
    else:
        return tool_run[result.tool].run(result.tool_input)

def execute():
    prompt = ChatPromptTemplate.from_messages([
        ('system', 'Você é um assistente amigável chamado Vinícius.'),
        ('user', '{input}'),
    ])

    chat = ChatOpenAI(model='gpt-3.5-turbo-0125')

    chain = prompt | chat.bind(functions=tools_json) | OpenAIFunctionsAgentOutputParser() | routing

    result = chain.invoke({ 'input': 'O que é uma mitocôndria?' })

    print(f'Resultado: {result}')
