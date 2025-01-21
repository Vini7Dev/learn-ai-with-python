from langchain.prompts import PromptTemplate
from langchain_openai.llms import OpenAI

def execute():
    template_word_count = PromptTemplate.from_template('''
    Responda a pergunta em até {max_words} palavras.
    ''', partial_variables={'max_words': 10})

    template_language = PromptTemplate.from_template('''
    Retorne a resposta em {language}.
    ''', partial_variables={'language': 'inglês'})

    prompt_template_final = (
        template_word_count
        + template_language
        + 'Responda a pergunta seguindo as instruções: {question}'
    )
    print(prompt_template_final.template)

    prompt_with_values = prompt_template_final.format(max_words=15, language='espanhol', question="Qual o nome da nossa lua?")
    print(prompt_with_values)

    llm = OpenAI()
    response = llm.invoke(prompt_with_values)
    print(f'Resposta: {response}')
