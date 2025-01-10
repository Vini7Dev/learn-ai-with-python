import os

import openai

WHISPER_MODEL = 'whisper-1'
TEXT_RESPONSE_FORMAT = 'text'
PORTUGUESE_LANG = 'pt'

openai_key = os.getenv('OPENAI_API_KEY')

def transcript_audio(audio_bytes, prompt = ''):
    client = openai.Client(api_key=openai_key)

    with open(str(audio_bytes), 'rb') as audio_file:
        transcription = client.audio.transcriptions.create(
            model=WHISPER_MODEL,
            language=PORTUGUESE_LANG,
            response_format=TEXT_RESPONSE_FORMAT,
            file=audio_file,
            prompt=prompt
        )
        return transcription
