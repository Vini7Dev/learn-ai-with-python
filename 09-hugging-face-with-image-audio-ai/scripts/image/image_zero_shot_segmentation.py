import matplotlib.pyplot as plt
import numpy as np
import cv2

import torch

from pathlib import Path
from PIL import Image
from transformers import CLIPSegProcessor, CLIPSegForImageSegmentation

def execute():
    image = Image.open(Path('assets/cities/city.jpg'))

    pretrained_name = 'CIDAS/clipseg-rd64-refined'
    processor = CLIPSegProcessor.from_pretrained(pretrained_name)
    model = CLIPSegForImageSegmentation.from_pretrained(pretrained_name)

    prompts = ['street', 'cars', 'traffc light']
    inputs = processor(
        text=prompts,
        images=[image] * len(prompts),
        padding=True,
        return_tensors='pt',
    )

    with torch.no_grad():
        outputs = model(**inputs)

    predictions = outputs.logits.unsqueeze(1)

    segmentations = []
    for i, label in enumerate(prompts):
        segmentations.append({
            'label': label,
            'mask': torch.sigmoid(predictions[i]).numpy(),
        })

    fig, axes = plt.subplots(nrows=1, ncols=len(prompts) + 1, figsize=(16, 4))

    axes[0].imshow(image)
    for i, segment in enumerate(segmentations):
        axes[i+1].imshow(segment['mask'], cmap='viridis')
        axes[i+1].set_title(segment['label'])

    plt.show()
