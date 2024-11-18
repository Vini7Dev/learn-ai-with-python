from dotenv import dotenv_values, find_dotenv

# from src.chat_stream import execute_chat
# from src.temperature_chat import execute_chat
from src.finance_chat_bot import execute_chat

env_vars = dotenv_values(find_dotenv())

chat_result = execute_chat(
    api_key=env_vars.get('OPENAI_API_KEY')
)

print(f'===> chat_result: {chat_result}')
