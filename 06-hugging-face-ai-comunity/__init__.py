from dotenv import load_dotenv, find_dotenv

# from scripts.fill_mask_model import execute
# from scripts.tokenizer_transformers import execute
# from scripts.text_generation import execute
from scripts.inference_api import execute

_ = load_dotenv(find_dotenv())

execute()
