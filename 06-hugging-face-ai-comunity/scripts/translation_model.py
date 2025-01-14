from transformers import pipeline

def execute():
    model = 'facebook/mbart-large-50-many-to-many-mmt'
    translator = pipeline(task='translation', model=model)
    languages = ['en_XX', 'es_XX', 'fr_XX']
    messages = [
        'Olá! Estou aprendendo a programar em Python e a user modelos de inteligência artificial.',
        'Bom dia! Tudo bem com você?',
        'Três tigres tristes comeram três pratos de trigo',
    ]
    for language in languages:
        result = translator(messages, tgt_lang=language, src_lang='pt_XX')
        print(f'{language}: {result}')
