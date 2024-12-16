import requests
import openai
from PIL import Image

CHAT_GPT_MODEL = 'dall-e-3'
CHAT_GPT_MODEL_EDIT = 'dall-e-2'
IMAGE_SIZE = '1024x1024'
ONE_IMAGE = 1

def generate_image(client: openai.Client, prompt: str):
    return client.images.generate(
        model=CHAT_GPT_MODEL,
        size=IMAGE_SIZE,
        n=ONE_IMAGE,
        quality='hd',
        style='natural',
        prompt=prompt,
    )

# Site to mark where it will be edited: https://ai-image-editor.netlify.app/
def edit_image(client: openai.Client, original: str, mask: str, prompt: str):
    return client.images.edit(
        model=CHAT_GPT_MODEL_EDIT,
        size=IMAGE_SIZE,
        n=ONE_IMAGE,
        prompt=prompt,
        image=open(original, 'rb'),
        mask=open(mask, 'rb'),
    )

def create_variation(client: openai.Client, file_name: str):
    return client.images.create_variation(
        size=IMAGE_SIZE,
        n=ONE_IMAGE,
        image=open(file_name, 'rb'),
    )

def save_image(image_generated):
    image_url = image_generated.data[0].url

    image_data = requests.get(image_url).content

    file_name = f'src/files/images/image_{CHAT_GPT_MODEL}.jpg'

    with open(file_name, 'wb') as f:
        f.write(image_data)

    return file_name

def open_image(file_name: str):
    image = Image.open(file_name)

    image.show()

def execute(api_key: str, action='GENERATE'):
    client = openai.Client(api_key=api_key)

    image_generated = None

    if action == 'GENERATE':
        prompt = 'Crie uma imagem de um bosque amplo com árvores floridas.'

        image_generated = generate_image(client=client, prompt=prompt)

    elif action == 'EDIT':
        prompt = 'Adicione um castor na imagem fornecida.'

        image_generated = edit_image(
            client=client,
            original='src/files/images/original.png',
            mask='src/files/images/mask.png',
            prompt=prompt,
        )

    elif action == 'VARIATION':
        image_generated = create_variation(
            client=client,
            file_name='src/files/images/original.png',
        )

    file_name = save_image(image_generated)

    open_image(file_name=file_name)

    return file_name
