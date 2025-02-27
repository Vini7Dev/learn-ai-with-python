from transformers import pipeline
from pathlib import Path
from PIL import Image

def execute():
    model = 'caidas/swin2SR-lightweight-x2-64'
    ampliator = pipeline('image-to-image', model=model)

    image = Image.open(Path('assets/animals/animal1.jpeg'))
    print(f'Original size: {image.size}')

    upscaled_image = ampliator(image)
    print(f'New size: {upscaled_image.size}')
