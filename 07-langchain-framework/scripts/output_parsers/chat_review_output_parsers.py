from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_openai.chat_models import ChatOpenAI

CUSTOMER_REVIEW = '''Este soprador de folhas é bastante incrível. Ele tem
quatro configurações: sopro de vela, brisa suave, cidade ventosa
e tornado. Chegou em dois dias, bem a tempo para o presente de
aniversário da minha esposa. Acho que minha esposa gostou tanto
que ficou sem palavras. Até agora, fui o único a usá-lo, e tenho
usado em todas as manhãs alternadas para limpar as folhas do
nosso gramado. É um pouco mais caro do que os outros sopradores
de folhas disponíveis no mercado, mas acho que vale a pena pelas
características extras.'''

def execute():
    is_gift_schema = ResponseSchema(
        description='O item foi comprado para alguém? True caso verdadeiro e False caso falso ou não tenha a informação.',
        name='is_gift',
        type='bool',
    )
    shipping_days_left_schema = ResponseSchema(
        description='Quantos dias para a entrega chegar? Se a resposta não for encontrada, retorne -1.',
        name='shippings_days_left',
        type='int'
    )
    perception_value_schema = ResponseSchema(
        description='Extraia qualquer frase sobre o valor ou preço do produto. Retorne como uma lista de Python.',
        name='perception_value',
        type='list'
    )
    response_schema = [
        is_gift_schema,
        shipping_days_left_schema,
        perception_value_schema
    ]

    output_parser = StructuredOutputParser.from_response_schemas(response_schema)
    formatted_schema = output_parser.get_format_instructions()

    review_template = ChatPromptTemplate.from_template('''
    Para o texto a seguir, extraia as seguintes informações:

    is_gift_schema, shipping_days_left_schema e perception_value_schema

    Texto: {review}

    {schema}
    ''')

    prompt_with_values = review_template.format_messages(
        schema=formatted_schema,
        review=CUSTOMER_REVIEW,
    )
    print(prompt_with_values)

    chat = ChatOpenAI()
    response = chat.invoke(prompt_with_values)
    print(f'Resposta: {response.content}')

    json_response = output_parser.parse(response.content)
    print(json_response)
