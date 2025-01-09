import openai

def get_response_stream(messages, api_key, model='gpt-3.5-turbo', temperature=0):
    openai.api_key = api_key
    response_stream = openai.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=messages,
        stream=True,
    )
    return response_stream
