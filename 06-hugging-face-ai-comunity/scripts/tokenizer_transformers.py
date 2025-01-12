from transformers import AutoTokenizer, AutoModel

def execute():
    model_name = 'FacebookAI/xlm-roberta-base'
    model = AutoModel.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    tokens = tokenizer('A linguagem <mask> é uma ferramenta inovadora.')
    inputs = tokenizer('A linguagem <mask> é uma ferramenta inovadora.', return_tensors='pt')
    outputs = model(**inputs)

    print(f'Tokens: {tokens}')
    print(f'Inputs: {inputs}')
    print(f'Outputs: {outputs}')
