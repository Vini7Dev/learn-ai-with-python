from pathlib import Path
from dotenv import load_dotenv, find_dotenv
import streamlit as st

from services.openai_audio import transcript_audio
from utils.get_microphone_audio import get_microphone_audio
from utils.convert_video_to_audio import convert_video_to_audio

TEMP_FOLDER = Path(__file__).parent / 'temp'
TEMP_FOLDER.mkdir(exist_ok=True)
AUDIO_TEMP_FILE = TEMP_FOLDER / 'audio_temp.mp3'
VIDEO_TEMP_FILE = TEMP_FOLDER / 'video_temp.mp4'
MIC_TEMP_FILE = TEMP_FOLDER / 'mic_temp.mp4'

_ = load_dotenv(find_dotenv())

def main():
    inicialization()
    main_page()

def inicialization():
    if not 'transcription' in st.session_state:
        st.session_state.transcription = ''

def main_page():
    st.header('Bem-vindo ao Asimov Transcript 🎙️', divider=True)
    st.markdown('#### Transcreva áudio do microfone, de vídeos e de arquivos de áudio')
    tab_mic, tab_video, tab_audio = st.tabs(['Microfone', 'Vídeo', 'Áudio'])
    with(tab_mic):
        transcript_tab_mic()
    with(tab_video):
        transcript_tab_video()
    with(tab_audio):
        transcript_tab_audio()

def transcript_tab_mic():
    prompt_input = st.text_input('(opcional) Digite o seu prompt...', key='input_mic')
    get_microphone_audio(mic_file=MIC_TEMP_FILE)
    if not MIC_TEMP_FILE.exists():
        return
    transcription = transcript_audio(audio_bytes=MIC_TEMP_FILE, prompt=prompt_input)
    st.session_state['transcription'] += transcription
    _render_transcription(transcription=st.session_state['transcription'])

def transcript_tab_video():
    prompt_input = st.text_input('(opcional) Digite o seu prompt...', key='input_video')
    video_file = st.file_uploader('Adicione um arquivo de vídeo ".mp4"', type=['mp4'])



    if not video_file is None:
        convert_video_to_audio(
            video_file=video_file,
            video_bytes=VIDEO_TEMP_FILE,
            audio_path=str(AUDIO_TEMP_FILE),
        )
        transcription = transcript_audio(audio_bytes=AUDIO_TEMP_FILE, prompt=prompt_input)
        _render_transcription(transcription=transcription)

def transcript_tab_audio():
    prompt_input = st.text_input('(opcional) Digite o seu prompt...', key='input_audio')
    audio_file = st.file_uploader('Adicione um arquivo de áudio ".mp3"', type=['mp3'])

    if not audio_file is None:
        with open(AUDIO_TEMP_FILE, 'wb') as f:
            f.write(audio_file.read())
        transcription = transcript_audio(audio_bytes=AUDIO_TEMP_FILE, prompt=prompt_input)
        _render_transcription(transcription=transcription)

def _render_transcription(transcription: str):
    st.markdown('*Transcrição*')
    st.write(transcription)
    st.session_state.transcription = transcription

if __name__ == '__main__':
    main()
