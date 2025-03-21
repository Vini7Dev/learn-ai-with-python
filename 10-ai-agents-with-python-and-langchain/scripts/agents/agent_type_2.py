from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai.chat_models import ChatOpenAI
from langchain_experimental.tools import PythonAstREPLTool

def execute():
    tools = [PythonAstREPLTool()]

    prompt = hub.pull('hwchase17/react')

    chat = ChatOpenAI()

    agent = create_react_agent(chat, tools, prompt)

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    result = agent_executor.invoke({'input': 'Qual é o décimo valor da sequência Fibonacci?'})

    print(f'Resultado: {result}')
