from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.chains.sequential import SequentialChain
from langchain_openai.chat_models import ChatOpenAI

def execute():
    chat = ChatOpenAI(model='gpt-3.5-turbo-0125')

    prompt_solve_question = PromptTemplate.from_template('''
    Resolva a questão fornecida para você.

    {question}

    Resolva com calma e passo a passo.
    ''')

    chain_solve_question = LLMChain(
        llm=chat,
        prompt=prompt_solve_question,
        output_key='correct_solution',
        verbose=True,
    )

    prompt_validate_student_solution = PromptTemplate.from_template('''
    ========
    Dado o seguinte problema:
    {question}
    ========
    Aqui está a solução correta:
    {correct_solution}
    ========
    Aqui está a solução do aluno para esse mesmo problema:
    {student_solution}
    ========
    Compare a solução do aluno com a solução correta que te informei, e verifique se
    o valor final que o aluno respondeu está igual.
    Se estiver diferente, então a resposta está incorreta.
    ''')

    chain_validate_student_solution = LLMChain(
        llm=chat,
        prompt=prompt_validate_student_solution,
        output_key='validation_result',
        verbose=True,
    )

    chain_main = SequentialChain(
        chains=[chain_solve_question, chain_validate_student_solution],
        input_variables=['question', 'student_solution'],
        output_variables=['correct_solution', 'validation_result'],
    )

    question = '''
    Pergunta:
    Estou construindo uma instalação de energia solar e preciso de ajuda com as contas de custos as finanças.
    - O terreno custa R$ 100 / metro quadrado
    - Posso comprar painéis solares por R$ 250 / metro quadrado
    - Negociei um contrato de manutenção que me custará R$ 100 mil por ano e  R$ 10 adicionais por metro quadrado

    Qual é o custo total para o primeiro ano de operações
    em função do número de metros quadrados.
    '''

    student_solution = '''
    Seja x o tamanho da instalação em metros quadrados.
    Custos:
    1. Custo do terreno: 100x
    2. Custo do painel solar: 250x
    3. Custo de manutenção: 100.000 + 100x
    Custo total: 100x + 250x + 100.000 + 100x = 450x + 100.000
    '''

    result = chain_main.invoke({
        'question': question,
        'student_solution': student_solution,
    })
    print(f'Resultado: {result}')
