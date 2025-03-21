from dotenv import find_dotenv, load_dotenv

# from scripts.lcel_langchain_expression_language.lcel import execute

# from scripts.external_functions.model_external_functions import execute
# from scripts.external_functions.tagging_functions_data_interpretation import execute
# from scripts.external_functions.text_extration import execute

# from scripts.tools.get_current_temperature import execute
# from scripts.tools.wikipedia_search import execute
# from scripts.tools.some_native_tools import execute

# from scripts.agents.agent_example import execute
# from scripts.agents.agent_executor import execute
# from scripts.agents.agent_type_1 import execute
# from scripts.agents.agent_type_2 import execute
from scripts.agents.agent_toolkit import execute

# from scripts.challenges.challenge1 import execute
# from scripts.challenges.challenge2 import execute
# from scripts.challenges.challenge3 import execute

_ = load_dotenv(find_dotenv())

execute()
