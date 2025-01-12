from transformers import pipeline

def execute():
    phrase = 'The capital of <mask> is Brasilia.'
    model = pipeline('fill-mask')
    predictions = model(phrase)

    for prediction in predictions:
        response = prediction['token_str']
        phrase_complete = prediction['sequence']
        score = prediction['score']
        score = score * 100
        print(f'Score: {score:.2f} | Predição: {response} | Phrase: {phrase_complete}')
