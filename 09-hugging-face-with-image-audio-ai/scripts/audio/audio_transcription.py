from transformers import pipeline
from datasets import load_dataset

def execute():
    dataset_name = 'PolyAI/minds14'
    dataset_lang = 'pt-PT'
    data = load_dataset(dataset_name, name=dataset_lang, split='train[:5]', trust_remote_code=True)

    # task = 'transcribe'
    task = 'translate'

    model_name = 'openai/whisper-medium'
    audio_transcriber = pipeline(
        'automatic-speech-recognition',
        model=model_name,
        generate_kwargs={ 'task': task, 'language': 'portuguese' },
    )

    transcription = audio_transcriber(data[0]['audio'])
    print(f'Transcrição: {transcription}')
