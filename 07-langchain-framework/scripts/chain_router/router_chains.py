from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from pydantic import BaseModel, Field

class Categorizator(BaseModel):
    '''Categoriza as perguntas de alunos do ensino fundamental'''
    area: str = Field(description='A área de conhecimento da pergunta feita pelo aluno. \
                      Deve ser "física", "matemática" ou "história". Caso não se encaixe \
                      em nenhuma delas, retorne "outra".')

def execute():
    chat_model = ChatOpenAI(model='gpt-4o-mini')

    phys_prompt = ChatPromptTemplate.from_template('''Você é um professor de física muito inteligente.
    Você é ótimo em responder perguntas sobre física de forma concisa
    e fácil de entender.
    Quando você não sabe a resposta para uma pergunta, você admite
    que não sabe.

    Aqui está uma pergunta: {question}''')

    math_prompt = ChatPromptTemplate.from_template('''Você é um matemático muito bom.
    Você é ótimo em responder perguntas de matemática.
    Você é tão bom porque consegue decompor
    problemas difíceis em suas partes componentes,
    responder às partes componentes e depois juntá-las
    para responder à pergunta mais ampla.

    Aqui está uma pergunta: {question}''')

    hist_prompt = ChatPromptTemplate.from_template('''Você é um historiador muito bom.
    Você tem um excelente conhecimento e compreensão de pessoas,
    eventos e contextos de uma variedade de períodos históricos.
    Você tem a capacidade de pensar, refletir, debater, discutir e
    avaliar o passado. Você tem respeito pela evidência histórica
    e a capacidade de usá-la para apoiar suas explicações
    e julgamentos.

    Aqui está uma pergunta: {question}''')

    default_prompt = ChatPromptTemplate.from_template('''{question}''')

    phys_chain = phys_prompt | chat_model
    math_chain = math_prompt | chat_model
    hist_chain = hist_prompt | chat_model
    default_chain = default_prompt | chat_model

    def router(input):
        if input['category'].area == 'matemática':
            return math_chain
        if input['category'].area == 'física':
            return phys_chain
        if input['category'].area == 'história':
            return hist_chain
        return default_chain

    categorizer_prompt = ChatPromptTemplate.from_template('Você deve categorizar a seguinte pergunta: {question}')

    struct_model = categorizer_prompt | chat_model.with_structured_output(Categorizator)
    # response = struct_model.invoke('Quanto é 1 + 1?')

    chain = RunnablePassthrough().assign(category=struct_model) | router
    response = chain.invoke({ 'question': 'Quando foi a independência do Brasil?' })

    print(f'Resposta: {response}')
