from langchain.prompts import ChatPromptTemplate
from langchain_openai.chat_models import ChatOpenAI

def execute():
    chat_template = ChatPromptTemplate.from_template('Essa é  aminha dúvida: {question}')
    template_with_vales = chat_template.format_messages(question='Quem sou eu?')
    print(template_with_vales, end='\n\n')

    chat_template = ChatPromptTemplate.from_messages(
        [
            ('system', 'Você é um assistente engraçado que se chama {assistant_name}'),
            ('human', 'Olá, como vai?'),
            ('ai', 'Melhor agora! Como posso ajudá-lo?'),
            ('human', '{question}'),
        ]
    )
    template_with_vales = chat_template.format(
        assistant_name='Jorge',
        question='Qual é o seu nome?',
    )
    print(template_with_vales, end='\n\n')

    chat = ChatOpenAI()
    response = chat.invoke(template_with_vales)
    print(f'Resposta: {response}')
