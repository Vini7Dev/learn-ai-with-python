from dotenv import load_dotenv, find_dotenv

# from scripts.models.llms import execute
# from scripts.models.chat_models import execute
# from scripts.models.chat_prompt_few_shot import execute
# from scripts.models.using_huggingface_models import execute
# from scripts.models.debug_langchain import execute
from scripts.models.caching import execute

_ = load_dotenv(find_dotenv())

execute()
