import sounddevice as sd
from transformers import pipeline
from datasets import load_dataset

def execute():
    dataset_name = 'google/fleurs'
    dataset_language = 'pt_br'
    dataset = load_dataset(dataset_name, name=dataset_language, split='train', streaming=True, trust_remote_code=True)

    model_name = 'sanchit-gandhi/whisper-medium-fleurs-lang-id'
    audio_classificator = pipeline('audio-classification', model_name)

    print(f'Sampling Rate do modelo: {audio_classificator.feature_extractor.sampling_rate}')

    first_rows = dataset.take(5)
    first_rows = list(first_rows)
    row = first_rows[0]
    audio = row['audio']['array']
    prediction = audio_classificator(audio.copy())
    print(f'Resultado: {prediction}')

    # Record my Microphone
    print('Gravando o microfone...')
    duration = 5
    sampling_rate = 16000
    vector_size = int(duration * sampling_rate)
    record = sd.rec(vector_size, samplerate=sampling_rate, channels=1)
    sd.wait()
    record = record.ravel()
    print('Fim!')

    prediction = audio_classificator(record)
    print(f'Resultado: {prediction}')
