from langchain_openai.chat_models import OpenAI

def execute():
    llm = OpenAI()

    question = 'Quanto é 2 vezes 3?'
    response = llm.invoke(question)
    print(f'Resposta: {response}')

    input()

    question = 'Conte uma breve história sobre a jornada de aprender a programar.'
    print('Resposta: ', end='')
    for part in llm.stream(question):
        print(part, end='')

    input()

    questions = [
        'O que é o céu?',
        'O que é a terra?',
        'O que são as estrelas?',
    ]
    responses = llm.batch(questions)
    print(f'Respostas: {responses}')
