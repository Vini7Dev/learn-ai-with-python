import openai
import time

CHAT_GPT_MODEL = 'gpt-3.5-turbo-0125'

def create_assistant(client):
    return client.beta.assistants.create(
        name='Tutor de Matemática da Asimov',
        instructions='Você é um tutor pessoal de matemática da emprsa Asimov. \
            Escreva e execute códigos para responder as perguntas de matemática que lhe forem passadas.',
        tools=[{ 'type': 'code_interpreter' }],
        model=CHAT_GPT_MODEL,
    )

def create_thread(client):
    return client.beta.threads.create()

def create_thread_message(client, thread, content, role = 'user'):
    return client.beta.threads.messages.create(
        thread_id=thread.id,
        role=role,
        content=content,
    )

def run_thread(client, assistant, thread):
    run = client.beta.threads.runs.create(
        assistant_id=assistant.id,
        thread_id=thread.id,
        instructions='O nome do usuário é Vinícius Gabriel, e ele é um usuário premium.'
    )

    while run.status in ['queued', 'in_progress', 'cancelling']:
        time.sleep(1)

        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )

    if run.status == 'completed':
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )

        return { 'run': run, 'messages': messages }

    return 'ERROR!'

def get_thread_steps(client, thread, run):
    return client.beta.threads.runs.steps.list(
        thread_id=thread.id,
        run_id=run.id,
    )

def execute_assistant(api_key):
    question = 'Se eu jogar um dado honesto 1000 vezes, qual é a probabilidade de eu obter exatamente 150 vezes o número 6? Resolva com um código.'

    client = openai.Client(api_key=api_key)

    assistant = create_assistant(client=client)

    thread = create_thread(client=client)

    create_thread_message(
        client=client,
        thread=thread,
        content=question,
    )

    thread_run = run_thread(
        client=client,
        assistant=assistant,
        thread=thread,
    )

    run_steps = get_thread_steps(
        client=client,
        thread=thread,
        run=thread_run['run'],
    )

    return {
        'run': thread_run['run'],
        'messages': thread_run['messages'],
        'steps': run_steps,
    }
