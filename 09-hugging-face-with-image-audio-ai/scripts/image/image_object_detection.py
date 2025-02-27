from pathlib import Path
from PIL import Image
from transformers import pipeline

from utils.display_object_detection import display_object_detection

def execute():
    model = 'facebook/detr-resnet-50'
    threshold = 0.9
    detector = pipeline('object-detection', model=model, threshold=threshold)

    image = Image.open(Path('assets/cities/city.jpg'))
    detections = detector(image)

    print(f'Detecções: {detections}')

    display_object_detection(image=image, detections=detections)
