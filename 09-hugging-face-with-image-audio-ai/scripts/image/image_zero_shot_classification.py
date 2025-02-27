from pathlib import Path
from PIL import Image
from transformers import pipeline

from utils.display_image import display_image

def execute():
    model = 'openai/clip-vit-large-patch14'
    clssificator = pipeline('zero-shot-image-classification', model=model)

    animals = [Image.open(file) for file in Path('assets/animals').iterdir()]
    classes = [
        'wolf',
        'tiger',
        'dog',
        'cat',
        'puma',
        'turtle',
        'bird',
    ]

    for i, image in enumerate(animals):
        predictions = clssificator(image, candidate_labels=classes)
        print(f'===> Predições {i+1} <===')
        for p in predictions:
            print(f'[{p['score'] * 100:.2f}%] {p['label']}')
        display_image(image)
