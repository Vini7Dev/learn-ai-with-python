from langchain_community.agent_toolkits.file_management.toolkit import FileManagementToolkit
from langchain_experimental.tools.python.tool import PythonREPLTool
from langchain.agents import load_tools

def execute():
    tool = PythonREPLTool()
    print(f'Descrição: {tool.description}')
    print(f'Argumentos: {tool.args}')
    print(f'Resultado: {tool.run({'query': 'print("Hello World!")'})}')
    print('======================')

    tools = load_tools(['stackexchange'])
    print(f'Descrição: {tools[0].description}')
    print(f'Argumentos: {tools[0].args}')
    print(f'Resultado: {tools[0].run({'query': 'How to print a message with Pascal?'})}')
    print('======================')

    tool_kit = FileManagementToolkit(
        root_dir='files',
        # selected_tools=['write_file', 'read_file', 'file_search', 'list_directory'],
    )
    tools = tool_kit.get_tools()
    for tool in tools:
        print(f'Name: {tool.name}')
        print(f'Descrição: {tool.description}')
        print(f'Argumentos: {tool.args}')
        print('---')
