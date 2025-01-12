from transformers import pipeline

MODELS = [
    { 'name': 'FacebookAI/xlm-roberta-base', 'token': '<mask>' },
    { 'name': 'neuralmind/bert-base-portuguese-cased', 'token': '[MASK]' },
    { 'name': 'rufimelo/Legal-BERTimbau-base', 'token': '[MASK]' },
]

def execute():

    for model in MODELS:
        model_name = model['name']
        model_token = model['token']
        print(f'MODEL: {model_name}')

        phrase = f'Este documento é essencial para a {model_token}.'
        model = pipeline(task='fill-mask', model=model_name)
        predictions = model(phrase)
        for prediction in predictions:
            response = prediction['token_str']
            phrase_complete = prediction['sequence']
            score = prediction['score']
            score = score * 100
            print(f'Score: {score:.2f} | Predição: {response} | Phrase: {phrase_complete}')
        input('Aperte "Enter" para ir para o próximo modelo.')
