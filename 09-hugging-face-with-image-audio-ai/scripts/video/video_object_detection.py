import cv2
import numpy as np
import matplotlib.pyplot as plt
from transformers import pipeline
from datasets import load_dataset
from matplotlib import patches
from matplotlib import colormaps
from PIL import Image

def cv2_to_pillow(array):
    array = cv2.cvtColor(array, cv2.COLOR_BGR2RGB)
    return Image.fromarray(array)

def plot_detection(image, detection, colormap='viridis'):
    labels = {det['label'] for det in detection}
    color_idexes = np.linspace(0, 1, len(labels))
    colors = [colormaps.get_cmap(colormap)(x) for x in color_idexes]
    colors = dict(zip(labels, colors))

    fig, ax = plt.subplots(figsize=(12, 12))
    ax.imshow(image)

    for det in detection:
        box = det['box']
        cor = colors[det['label']]
        origin = (box['xmin'], box['ymin'])
        width = box['xmax'] - box['xmin']
        height = box['ymax'] - box['ymin']

        rect = patches.Rectangle(origin, width, height, linewidth=3, edgecolor=cor, facecolor='none')
        ax.add_patch(rect)

        text = f'{det["label"]} {100 * det["score"]:.2f}%'
        ax.text(box['xmin'], box['ymin'] - 15, text, bbox={'facecolor': cor, 'alpha': 0.8})
    return ax

def execute():
    model = 'facebook/detr-resnet-50'
    detector = pipeline('object-detection', model=model)

    data = load_dataset('shinonomelab/cleanvid-15m_map', streaming=True, split='train')

    video_index = 1
    video_row = [
        li
        for i, li in enumerate(data.take(20))
        if i == video_index
    ]

    if video_row:
        row_data = video_row[0]
        url = row_data['videourl']
        fps = int(row_data['framerate'])
        frame_count = 0
        print(f'===> Vídeo: {url}')
        capture = cv2.VideoCapture(url)
        success, frame = capture.read()
        while success:
            image = cv2_to_pillow(frame)
            if frame_count % fps == 0:
                detection = detector(image)
                ax = plot_detection(image=image, detection=detection, colormap='rainbow')
                ax.set_title(f'Frame {frame_count}')
            success, frame = capture.read()
            frame_count += 1
        plt.show()
