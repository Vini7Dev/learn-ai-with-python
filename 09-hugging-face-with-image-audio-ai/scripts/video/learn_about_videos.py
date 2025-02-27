import cv2
from pathlib import Path

def execute():
    frames_folder = Path('assets/videos/frames')
    videos_folder = Path('assets/videos/')

    video_path = videos_folder / 'video.mp4'

    capture = cv2.VideoCapture(str(video_path))
    success, frame = capture.read()
    fps = int(capture.get(cv2.CAP_PROP_FPS))
    count = 0

    while success:
        if count % fps == 0:
            frame_name = f'frame{count:03d}.jpg'
            cv2.imwrite(str(frames_folder / frame_name), frame)
            print('.', end='')
        success, frame = capture.read()
        count += 1
    print('Finalizado!')
