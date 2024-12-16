from dotenv import dotenv_values, find_dotenv

# from src.text_generation_scripts.chat_stream import execute_chat
# from src.text_generation_scripts.temperature_chat import execute_chat
# from src.text_generation_scripts.finance_chat_bot import execute_chat
# from src.text_generation_scripts.fine_tuning import execute
# from src.text_generation_scripts.use_fine_tuning import execute

# from src.assistants_api.math_assistant import execute_assistant
# from src.assistants_api.finance_assistant import execute_assistant
# from src.assistants_api.attendant_assistant import execute_assistant

from src.work_with_images.image_generator import execute

env_vars = dotenv_values(find_dotenv())

'''
chat_result = execute_chat(
    api_key=env_vars.get('OPENAI_API_KEY')
)

print(f'===> chat_result: {chat_result}')
'''

'''
fine_tuning_result = execute(
    api_key=env_vars.get('OPENAI_API_KEY'),
    action="get-jobs",
    # action="create-job",
)

print(f'===> fine_tuning_result: {fine_tuning_result}')
'''

'''
use_fine_tuning_result = execute(api_key=env_vars.get('OPENAI_API_KEY'))

print(f'===> use_fine_tuning_result: {use_fine_tuning_result}')
'''

'''
result = execute_assistant(api_key=env_vars.get('OPENAI_API_KEY'))

print(f'===> result status: {result['run'].status}')
print(f'===> result message: {result['messages'].data[0].content[0].text.value}')

for step in result['steps'].data[::-1]:
    print(f'===> step: {step.step_details.type}')
    if step.step_details.type == 'tool_calls':
        for tool_call in step.step_details.tool_calls:
            print(f'=> tool call input: {tool_call.code_interpreter.input}')
            print(f'=> tool call outputs: {tool_call.code_interpreter.outputs}')
'''

'''
result = execute_assistant(api_key=env_vars.get('OPENAI_API_KEY'))

print(f'===> Result: {result}')
'''

result = execute(
    api_key=env_vars.get('OPENAI_API_KEY'),
    action='VARIATION',
)

print(f'===> Result: {result}')
