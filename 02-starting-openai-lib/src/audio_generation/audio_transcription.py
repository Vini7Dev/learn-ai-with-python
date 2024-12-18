import openai

AUDIO_GPT_MODEL = 'whisper-1'
VIDEO_CAPTION_FORMAT = 'srt'
LANG_PORTUGUESE = 'pt'

def execute(api_key: str):
    audio_file = open('src/files/audio/audio_asimov.mp3', 'rb')

    client = openai.Client(api_key=api_key)

    prompt = 'Essa é a transcrição de uma aula da Asimov Academy.\
        O professor se chama Rodrigo Soares Tadewald.'

    transcription = client.audio.transcriptions.create(
        model=AUDIO_GPT_MODEL,
        language=LANG_PORTUGUESE,
        response_format=VIDEO_CAPTION_FORMAT,
        file=audio_file,
        prompt=prompt,
    )

    return transcription
