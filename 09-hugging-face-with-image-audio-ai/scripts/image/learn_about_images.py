from datasets import load_dataset
import matplotlib.pyplot as plt
import numpy as np

def execute():
    data = load_dataset('cats_vs_dogs', split='train', streaming=True)

    image = list(data.take(5))[3]['image']

    print(f'Formato do arquivo: {image.format}')
    print(f'Modo : {image.mode}')
    print(f'Dimensões da imagem: {image.width} x {image.height}')

    image_data = np.array(image)
    print(f'Dados da imagem: {image_data}')
    print(f'Formação da imagem: {image_data.shape}')

    image_r = image_data[:, :, 0]
    image_g = image_data[:, :, 1]
    image_b = image_data[:, :, 2]
    print(f'Cor vermelha: {image_r}')
    print(f'Cor verde: {image_g}')
    print(f'Cor azul: {image_b}')

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(ncols=2, nrows=2)
    ax1.imshow(image)
    ax2.imshow(image_r, cmap='Reds')
    ax3.imshow(image_g, cmap='Greens')
    ax4.imshow(image_b, cmap='Blues')
    plt.show()

    image_pixel = image_data[200, 300, :]
    print(f'Pixel da imagem: {image_pixel}')

    image_data[200, 300, :] = np.array([255, 0, 0])
