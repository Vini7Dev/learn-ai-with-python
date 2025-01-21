from dotenv import load_dotenv, find_dotenv

# from scripts.llms import execute
from scripts.chat_models import execute

_ = load_dotenv(find_dotenv())

execute()
