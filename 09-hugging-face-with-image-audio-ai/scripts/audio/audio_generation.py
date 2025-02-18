import torch
from transformers import pipeline

def execute():
    model_name = 'suno/bark-small'
    reader = pipeline(
        'text-to-speech',
        model=model_name,
        forward_params={'max_new_tokens': 50},
        # Optimization
        model_kwargs={'torch_dtype': torch.float16},
    )

    # Optimization
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    reader.model = reader.model.to(device)
    reader.model = reader.model.to_bettertransformer()

    text = 'Olá! Meu nome é Vinícius e estou aprendendo Python!'
    audio = reader(text)

    print(f'Audio: {audio}')
