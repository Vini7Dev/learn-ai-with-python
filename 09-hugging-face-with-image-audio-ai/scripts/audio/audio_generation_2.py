import torch
from transformers import AutoProcessor, AutoModel

def execute():
    model_name = 'suno/bark-small'
    processor = AutoProcessor.from_pretrained(model_name, max_new_tokens=50)
    reader = AutoModel.from_pretrained(model_name)

    # Accepted voices: https://suno-ai.notion.site/8b8e8749ed514b0cbf3f699013548683?v=bc67cff786b04b50b3ceb756fd05f68c
    voice = 'v2/pt_speaker_1'
    text = 'Olá! Meu nome é Vinícius e estou aprendendo Python!'
    inputs = processor(text, voice_preset=voice)
    audio_vector = reader.generate(**inputs)
    result = {
        'audio': audio_vector.numpy(),
        'sampling_rate': reader.generation_config.sample_rate,
    }

    print(f'Audio: {result}')
