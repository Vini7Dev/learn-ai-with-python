import openai
import time

CHAT_GPT_MODEL = 'gpt-3.5-turbo-0125'

def execute_assistant(api_key: str):
    client = openai.Client(api_key=api_key)

    vector_store = client.beta.vector_stores.create(
        name='Apostilas Asimov Aula 15',
    )

    files = [
        'src/files/assistants/Explorando a API da OpenAI.pdf',
        'src/files/assistants/Explorando o Universo das IAs com Hugging Face.pdf',
    ]

    files_stream = [open(f, 'rb') for f in files]

    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id,
        files=files_stream,
    )

    assistant = client.beta.assistants.create(
        model=CHAT_GPT_MODEL,
        name='Tutor Asimov',
        instructions='Você é um tutor de uma escola de programação. Você é ótimo para \
            responder perguntas sobre a API da OpenAI e sobre a utilização da biblioteca \
            do Hugging Face com Python. Você utiliza as apostilas dos cursos para basear \
            suas respostas. Caso você não encontre as respostas nas apostilas informadas, \
            você fala que não sabe responder.',
        tools=[{ 'type': 'file_search' }],
        tool_resources={ 'file_search': { 'vector_store_ids': [vector_store.id] } },
    )

    thread = client.beta.threads.create()

    question_message = 'Segundo o documento fornecido, o que é o Hugging Face?'

    messages = client.beta.threads.messages.create(
        role='user',
        thread_id=thread.id,
        content=question_message,
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="O nome do usuário é Vinícius e ele é um usuário prémium."
    )

    while run.status in ['queued', 'in_progress', 'cancelling']:
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )

    if run.status != 'completed':
        return f'Error status: {run.status}'

    messages = client.beta.threads.messages.list(thread_id=thread.id)

    run_steps = client.beta.threads.runs.steps.list(
        thread_id=thread.id,
        run_id=run.id,
    )

    for step in run_steps.data[::-1]:
        try:
            print(f'\n ===> Step: {step.step_details.type}')
            if step.step_details.type == 'tool_calls':
                for tool_call in step.step_details.tool_calls:
                    if tool_call.type == 'file_search':
                        print(tool_call)
                    else:
                        print('-------')
                        print(tool_call.code_interpreter.input)
                        print('-------')
                        print('Result')
                        if tool_call.code_interpreter.outputs[0].type == 'logs':
                            print(tool_call.code_interpreter.outputs[0].logs)
            elif step.step_details.type == 'message_creation':
                message = client.beta.threads.messages.retrieve(
                    thread_id=thread.id,
                    message_id=step.step_details.message_creation.message_id,
                )
                if message.content[0].type == 'text':
                    print(f'Message: {message.content[0].text.value}')
                elif message.content[0].type == 'image_file':
                    file_id = message.content[0].image_file.file_id
                    image_data = client.files.content(file_id)
                    with open(f'src/files/assistants/finance-assistent-{file_id}.png', 'wb') as f:
                        f.write(image_data.read())
                        print(f'Saved finance-assistent-{file_id}.png image!')
        except:
            pass

    return messages
