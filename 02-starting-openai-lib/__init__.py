from dotenv import dotenv_values, find_dotenv

# from src.text_generation_scripts.chat_stream import execute_chat
# from src.text_generation_scripts.temperature_chat import execute_chat
# from src.text_generation_scripts.finance_chat_bot import execute_chat
from src.text_generation_scripts.fine_tuning import execute
from src.text_generation_scripts.use_fine_tuning import execute

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


use_fine_tuning_result = execute(api_key=env_vars.get('OPENAI_API_KEY'))

print(f'===> use_fine_tuning_result: {use_fine_tuning_result}')
