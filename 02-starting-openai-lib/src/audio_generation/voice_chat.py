from io import BytesIO
from pathlib import Path
import openai
from playsound import playsound
import speech_recognition as sr

GENERATE_AUDIO_GPT_MODEL = 'tts-1'
TRANSCRIPTION_GPT_MODEL = 'whisper-1'
CHAT_GPT_MODEL = 'gpt-3.5-turbo-0125'
VOICE_ECHO = 'echo'
CHAT_GPT_MAX_TOKENS = 1000
CHAT_GPT_TEMPERATURE = 1

def get_audio_transcription(client: openai.Client, audio):
    wav_data = BytesIO(audio.get_wav_data())
    wav_data.name = 'audio.wav'

    transcription = client.audio.transcriptions.create(
        model=TRANSCRIPTION_GPT_MODEL,
        file=wav_data,
    )

    return transcription.text

def get_chat_response(client: openai.Client, messages):
    response = client.chat.completions.create(
        model=CHAT_GPT_MODEL,
        max_tokens=CHAT_GPT_MAX_TOKENS,
        temperature=CHAT_GPT_TEMPERATURE,
        messages=messages,
    )
    return response.choices[0].message.content

def get_mic_audio(recognizer: sr.Recognizer):
    with sr.Microphone() as source:
        print('Ouvindo...')
        recognizer.adjust_for_ambient_noise(source=source, duration=1)
        mic_audio = recognizer.listen(source)

    return mic_audio

def create_audio_by_text(client: openai.Client, text: str):
    assistant_voice_file_name = 'src/files/audio/assistant_voice.mp3'

    response = client.audio.speech.create(
        model=GENERATE_AUDIO_GPT_MODEL,
        voice=VOICE_ECHO,
        input=text,
    )

    if (Path(assistant_voice_file_name).exists()):
        Path(assistant_voice_file_name).unlink()

    response.write_to_file(assistant_voice_file_name)

    return assistant_voice_file_name

def play_sound(file_name: str):
    playsound(file_name)

def execute(api_key: str):
    messages = []

    recognizer = sr.Recognizer()
    client = openai.Client(api_key=api_key)

    while True:
        mic_audio = get_mic_audio(recognizer=recognizer)

        mic_audio_transcription = get_audio_transcription(client=client, audio=mic_audio)

        print(f'User: {mic_audio_transcription}')

        messages.append({ 'role': 'user', 'content': mic_audio_transcription })

        chat_response = get_chat_response(client=client, messages=messages)

        assistant_voice_file = create_audio_by_text(client=client, text=chat_response)

        print(f'Assistant: {chat_response}')

        play_sound(file_name=assistant_voice_file)

        messages.append({ 'role': 'assistant', 'content': chat_response })
