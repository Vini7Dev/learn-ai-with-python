import queue
import time

import pydub
import streamlit as st
from streamlit_webrtc import WebRtcMode, webrtc_streamer

MAX_AUDIO_TIME_IN_SECONDS = 10

@st.cache_data
def get_ice_servers():
    return [{'urls': ['stun:stun.l.google.com:19302']}]

def get_microphone_audio(mic_file):
    webrtc_ctx = webrtc_streamer(
        key='get_mic_audio',
        mode=WebRtcMode.SENDONLY,
        audio_receiver_size=1024,
        media_stream_constraints={'video': False, 'audio': True},
        # rtc_configuration={'iceServers': get_ice_servers()},
    )
    if not webrtc_ctx.state.playing:
        st.write(st.session_state.transcription)
        return

    container = st.empty()
    container.markdown('Comece a falar...')
    audio_chunk = pydub.AudioSegment.empty()
    last_transcription_time = time.time()
    st.session_state['transcription'] = ''
    while True:
        if webrtc_ctx.audio_receiver:
            try:
                audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=1)
            except queue.Empty:
                time.sleep(0.1)
                continue
            container.markdown(f'Frames recebidos {len(audio_frames)}')

            for frame in audio_frames:
                sound = pydub.AudioSegment(
                    data=frame.to_ndarray().tobytes(),
                    sample_width=frame.format.bytes,
                    frame_rate=frame.sample_rate,
                    channels=len(frame.layout.channels)
                )
                audio_chunk += sound

            now_time = time.time()
            if len(audio_chunk) > 0 and now_time - last_transcription_time > MAX_AUDIO_TIME_IN_SECONDS:
                last_transcription_time = now_time
                audio_chunk.export(mic_file)
                audio_chunk = pydub.AudioSegment.empty()
        else:
            break

    #
