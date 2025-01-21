import langchain
from langchain.globals import set_llm_cache
from langchain.cache import InMemoryCache, SQLiteCache
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# In memory cache
# set_llm_cache(InMemoryCache())

# SQLite Cache
set_llm_cache(SQLiteCache(database_path='files/cache/langchain_cache_db.sqlite'))

def execute():
    message = [
        SystemMessage(content='Você é um assistente engraçado.'),
        HumanMessage(content='Quanto é 1 + 1?'),
    ]
    chat = ChatOpenAI(model='gpt-3.5-turbo-0125')
    response = chat.invoke(message)
    print(f'Resposta: {response}')
