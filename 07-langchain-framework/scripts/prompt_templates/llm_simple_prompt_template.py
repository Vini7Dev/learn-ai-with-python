from langchain.prompts import PromptTemplate

def execute():
    prompt_template = PromptTemplate.from_template('''
    Responda a seguinte pergunta do usuário em até {max_words} palavras:
    {question}
    ''', partial_variables={'max_words': 10})
    prompt_template.format(
        question='O que é um buraco negro?',
        max_words=10,
    )
    print(prompt_template)
