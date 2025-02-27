from pathlib import Path
from PIL import Image
from transformers import pipeline

from utils.display_object_detection import display_object_detection

def execute():
    model = 'google/owlv2-base-patch16-ensemble'
    threshold = 0.3
    detector = pipeline('zero-shot-object-detection', model=model, threshold=threshold)

    image = Image.open(Path('assets/cities/city.jpg'))

    classes = [
        'tree',
        'person',
        'building',
        'US flag',
        'crosswalk',
    ]

    detections = detector(image, candidate_labels=classes)
    print(f'Detecções: {detections}')

    display_object_detection(image=image, detections=detections)
