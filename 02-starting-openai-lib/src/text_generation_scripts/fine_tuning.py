import json
import openai

JSON_FILE_PATH = 'src/files/fine-tuning/chatbot_respostas.json'
JSON_L_FILE_PATH = 'src/files/fine-tuning/chatbot_respostas.jsonl'

def get_fine_tuning_json_examples():
    with open(JSON_FILE_PATH, encoding="utf8") as f:
        json_examples = json.load(f)

        return json_examples

def create_jsonl_examples_file(examples):
    with open(JSON_L_FILE_PATH, 'w', encoding="utf8") as f:
        for input in examples:
            response_example = {
                'origin': 'AsimovBot',
                'response': input['resposta'],
                'category': input['categoria'],
            }
            jsonl_input = {
                'messages': [
                    { 'role': 'user', 'content': input['pergunta'] },
                    { 'role': 'assistant', 'content': json.dumps(response_example, ensure_ascii=False, indent=2) },
                ]
            }
            json.dump(jsonl_input, f, ensure_ascii=False)
            f.write('\n')

def send_to_open_ai(client):
    file = client.files.create(
        file=open(JSON_L_FILE_PATH, 'rb'),
        purpose="fine-tune",
    )

    client.fine_tuning.jobs.create(
        training_file=file.id,
        model="gpt-3.5-turbo",
    )

    return file

def get_fine_tuning_jobs(client):
    return client.fine_tuning.jobs.list()

def execute(api_key, action="get-jobs"):
    client = openai.Client(api_key=api_key)

    if action == "get-jobs":
        return get_fine_tuning_jobs(client=client)

    elif action == "create-job":
        json_examples = get_fine_tuning_json_examples()

        create_jsonl_examples_file(json_examples)

        return send_to_open_ai(client=client)

    else:
        return "ACTION NOT FOUND!"
