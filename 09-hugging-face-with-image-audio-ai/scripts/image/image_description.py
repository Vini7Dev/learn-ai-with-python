from transformers import pipeline
from pathlib import Path
from PIL import Image

def execute():
    model = 'microsoft/git-large-coco'
    descriptor = pipeline('image-to-text', model=model)

    image = Image.open(Path('assets/animals/animal1.jpeg'))

    description = descriptor(image)
    print(f'Descrição: {description}')
