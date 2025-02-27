from pathlib import Path
from PIL import Image
from datasets import load_dataset
from transformers import pipeline
import matplotlib.pyplot as plt

from utils.display_image import display_image

def execute():
    model = 'akahana/vit-base-cats-vs-dogs'
    classificator = pipeline('image-classification', model=model)

    dataset = 'Bingsu/Cat_and_Dog'
    data = load_dataset(dataset, split='test')

    rows = data.shuffle()[:4]

    for image in rows['image']:
        prediction = classificator(image)
        print(f'Resultado: {prediction}')
        display_image(image)

    THRESHOLD = 0.5

    dog_images = [Image.open(file) for file in Path('assets/dogs').iterdir()]

    for image in dog_images:
        predictions = classificator(image)
        best_score = predictions[0]['score']
        best_label = predictions[0]['label']
        formated_score = f'{best_score * 100:.2f}%'
        if (best_score < THRESHOLD):
            print('O modelo não foi capaz de prever o resultado com uma confiança aceitável!')

        print(f'Resultado: {formated_score} = {best_label}')
        display_image(image)
