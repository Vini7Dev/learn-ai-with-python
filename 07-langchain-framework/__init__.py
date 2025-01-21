from dotenv import load_dotenv, find_dotenv

# from scripts.models.llms import execute
# from scripts.models.chat_models import execute
# from scripts.models.chat_prompt_few_shot import execute
# from scripts.models.using_huggingface_models import execute
# from scripts.models.debug_langchain import execute
# from scripts.models.caching import execute

# from scripts.prompt_templates.llm_simple_prompt_template import execute
# from scripts.prompt_templates.llm_compose_prompt_templates import execute
# from scripts.prompt_templates.chat_simple_prompt_template import execute
# from scripts.prompt_templates.llm_few_shot_prompting import execute
from scripts.prompt_templates.chat_few_shot_prompting import execute

_ = load_dotenv(find_dotenv())

execute()
