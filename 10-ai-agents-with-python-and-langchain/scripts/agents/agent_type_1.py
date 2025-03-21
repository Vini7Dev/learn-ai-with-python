from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from langchain_experimental.tools import PythonAstREPLTool

def execute():
    tools = [PythonAstREPLTool()]

    system_message = '''Você é um agente projetado para escrever e executar código Python para responder perguntas.
    Você tem acesso a um REPL Python, que pode usar para executar código Python.
    Se encontrar um erro, depure o código e tente novamente.
    Use apenas a saída do seu código para responder à pergunta.
    Você pode conhecer a resposta sem executar nenhum código, mas deve ainda assim executar o código para obter a resposta.
    Se não parecer possível escrever código para responder à pergunta, simplesmente retorne "Não sei" como a resposta.'''

    prompt = ChatPromptTemplate.from_messages([
        ('system', system_message),
        ('placeholder', '{chat_history}'),
        ('human', '{input}'),
        ('placeholder', '{agent_scratchpad}'),
    ])

    chat = ChatOpenAI()
    agent = create_tool_calling_agent(chat, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    result = agent_executor.invoke({'input': 'Qual é o décimo valor da sequência Fibonacci?'})

    print(f'Resultado: {result}')
