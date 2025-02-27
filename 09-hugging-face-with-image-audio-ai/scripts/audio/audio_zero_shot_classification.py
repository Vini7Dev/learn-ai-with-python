from transformers import pipeline
from datasets import Audio, load_dataset

def execute():
    dataset_name = 'ashraq/esc50'
    split = 'train[:5]'
    dataset = load_dataset(dataset_name, split=split)

    model_name = 'laion/clap-htsat-fused'
    audio_classificator = pipeline('audio-classification', model=model_name)

    model_sampling_rate = audio_classificator.feature_extractor.sampling_rate

    print(f'Sampling Rate do modelo: {model_sampling_rate}')

    dataset = dataset.cast_column('audio', Audio(sampling_rate=model_sampling_rate))
    labels = [
        'sound of a dog',
        'sound of a vacuum cleaner',
        'sound of birds',
        'sound of a cat',
        'sound of a cow',
    ]

    for row in dataset:
        prediction = audio_classificator(row['audio']['array'], candidate_labels=labels)
        print(f'Resultado: {prediction}', end='\n\n')
