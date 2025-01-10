from moviepy import VideoFileClip

def convert_video_to_audio(video_file, video_bytes, audio_path: str):
    with open(video_bytes, 'wb') as f:
        f.write(video_file.read())
    moviepy_video = VideoFileClip(str(video_bytes))
    moviepy_video.audio.write_audiofile(audio_path)
