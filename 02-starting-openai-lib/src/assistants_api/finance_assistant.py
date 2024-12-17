import openai
import time

CHAT_GPT_MODEL = 'gpt-3.5-turbo-0125'

def execute_assistant(api_key: str):
    client = openai.Client(api_key=api_key)

    file = client.files.create(
        file=open('src/files/assistants/supermarket_sales.csv', 'rb'),
        purpose='assistants',
    )

    assistant = client.beta.assistants.create(
        model=CHAT_GPT_MODEL,
        name="Analista Financeiro de Supermercado",
        instructions="Você é um analista de um supermercado. Você deve utilizar os dados .csv informados relativos às vendas do super mercado para realizar as suas análises.",
        tools=[{ 'type': 'code_interpreter' }],
        tool_resources={ 'code_interpreter': { 'file_ids': [file.id] } },
    )

    thread = client.beta.threads.create()

    # question_message = 'Qual é o rating médio das vendas do supermercado? O arquivo está no formato CSV.'
    question_message = 'Gere um gráfico pizza com o percentual de vendas por meio de pagamento. O arquivo está no formato CSV.'

    messages = client.beta.threads.messages.create(
        role='user',
        thread_id=thread.id,
        content=question_message,
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="O nome do usuário é Vinícius."
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
