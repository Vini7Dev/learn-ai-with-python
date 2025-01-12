from transformers import pipeline

def execute():
    system_message = 'You are the helpful artificial intelligence.'
    system_prompt = f'<|im_start|>system\n{system_message}<|im_end|>'
    full_input = system_prompt

    while True:
        user_message = input('Question: ')
        user_prompt = f'<|im_start|>user\n{user_message}<|im_end|>'
        full_input += f'{user_prompt}\n<|im_start|>assistant'

        chatbot = pipeline(
            task='text-generation',
            model='Felladrin/Llama-68M-Chat-v1',
            max_new_tokens=100,
            penalty_alpha=0.5,
            top_k=4,
        )
        response = chatbot(full_input)
        generated_text = response[0]['generated_text']
        full_input = generated_text
        bot_response = generated_text.split('<|im_start|>assistant\n')[-1].rstrip('<|im_end|>')
        print(f'Bot Response: {bot_response}')
