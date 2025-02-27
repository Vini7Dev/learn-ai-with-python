from transformers import pipeline
from datasets import load_dataset

def execute():
    dataset = 'shinonomelab/cleanvid-15m_map'
    data = load_dataset(dataset, streaming=True, split='train')

    model = 'facebook/timesformer-base-finetuned-k600'
    classificator = pipeline('video-classification', model=model)

    person_count = 0
    for row in data.take(5):
        if person_count >= 3:
            break
        person_count += 1

        categories = row['categories']
        if 'People' not in categories:
            continue

        video_url = row['videourl']
        predictions = classificator(video_url)
        print(f'=================================================')
        print(f'===> Vídeo: {video_url}')
        for prediction in predictions:
            print(f'> Predição: {prediction}')
