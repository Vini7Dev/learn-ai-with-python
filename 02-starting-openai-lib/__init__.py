from dotenv import load_dotenv, find_dotenv

import openai

_ = load_dodenv(find_dotenv())

client = openai.Client()
