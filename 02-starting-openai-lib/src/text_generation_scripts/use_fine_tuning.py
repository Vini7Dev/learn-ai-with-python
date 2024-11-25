import openai

TEMPERATURE = 0
MAX_TOKENS = 1000

# SYSTEM_MESSAGE = '''
# Responde as perguntas em um parágrafo de até 20 palavras. Categorize as respostas nos seguintes conteúdos: física, matemática, língua portuguesa ou outros.
# Retorne a resposta em um formato json, com as keys:
# origin: valor deve ser sempre AsimovBot
# response: a resposta para a pergunta
# category: a categoria da pergunta
# '''

'''
messages = [
    { 'role': 'system', 'content': SYSTEM_MESSAGE },
    { 'role': 'user', 'content': 'O que é uma equação quadrática?' },
]
'''

messages = [
    { 'role': 'user', 'content': 'O que é uma equação quadrática?' },
]

def execute(api_key):
    client = openai.Client(api_key=api_key)

    response = client.chat.completions.create(
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        messages=messages,
        model="ft:gpt-3.5-turbo-0125:personal::AVzy5lvC",
    )

    print('===> response', response.choices[0].message.content)

    return response
