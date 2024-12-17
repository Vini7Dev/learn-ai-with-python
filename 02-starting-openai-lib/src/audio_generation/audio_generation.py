import openai

AUDIO_GPT_MODEL = 'tts-1'
VOICE_ECHO = 'echo'

def create_audio(client: openai.Client, text: str, file_name: str):
    response = client.audio.speech.create(
        model=AUDIO_GPT_MODEL,
        voice=VOICE_ECHO,
        input=text,
    )

    response.write_to_file(file_name)

def create_audio_stream(client: openai.Client, text: str, file_name: str):
    with client.audio.speech.with_streaming_response.create(
        model=AUDIO_GPT_MODEL,
        voice=VOICE_ECHO,
        input=text,
    ) as response:
        response.stream_to_file(file_name)

def execute(api_key: str):
    client = openai.Client(api_key=api_key)

    file_name = 'src/files/audio/voice.mp3'

    text = '''
    Python é uma linguagem de programação de alto nível, interpretada de script, imperativa, orientada a objetos,
    funcional, de tipagem dinâmica e forte. Foi lançada por Guido van Rossum em 1991. Atualmente, possui um modelo
    de desenvolvimento comunitário, aberto e gerenciado pela organização sem fins lucrativos Python Software Foundation.
    Apesar de várias partes da linguagem possuírem padrões e especificações formais, a linguagem, como um todo, não é
    formalmente especificada. O padrão na pratica é a implementação CPython.
    '''

    create_audio_stream(client=client, text=text, file_name=file_name)
    # create_audio(client=client, text=text, file_name=file_name)

    return file_name
