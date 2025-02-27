import matplotlib.pyplot as plt
import numpy as np
import cv2

from pathlib import Path
from PIL import Image
from transformers import pipeline

def execute():
    model = 'nvidia/segformer-b1-finetuned-cityscapes-1024-1024'
    segmenter = pipeline('image-segmentation', model=model)

    image = Image.open(Path('assets/cities/city.jpg'))

    segmentation = segmenter(image)

    print(f'===> Segmentação: {segmentation}')

    imgae_copy = image.copy()
    imgae_copy.thumbnail((300, 300))
    image_mask = segmentation[0]['mask']
    image_mask.thumbnail((300, 300))

    fig, ((ax1, ax2)) = plt.subplots(ncols=2, nrows=1)
    ax1.imshow(imgae_copy)
    ax2.imshow(image_mask)
    plt.show()

    image_data = np.array(imgae_copy)
    mask_data = np.array(segmentation[0]['mask'])
    masked_image = image_data & mask_data[:, :, np.newaxis]
    plt.imshow(masked_image)
    plt.show()

    inversed_mask_image = np.bitwise_not(mask_data)
    inversed_masked_image = image_data & inversed_mask_image[:, :, np.newaxis]
    plt.imshow(inversed_masked_image)
    plt.show()

    green_color = np.array([0, 255, 0])
    image_mask = image_data.copy()
    image_mask = np.where(mask_data[:, :, np.newaxis] == 255, green_color, image_mask)
    image_mask = image_mask.astype(image_data.dtype)
    plt.imshow(image_mask)
    plt.show()

    combined_image = cv2.addWeighted(image_data, 0.5, image_mask, 0.5, 0)
    plt.imshow(combined_image)
    plt.show()
