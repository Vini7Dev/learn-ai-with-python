from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.chains.router import MultiPromptChain
from langchain.chains.llm import LLMChain
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_openai.chat_models import ChatOpenAI

def execute():
    chat = ChatOpenAI(model='gpt-3.5-turbo-0125')

    phys_template = ChatPromptTemplate.from_template('''Você é um professor de física muito inteligente.
    Você é ótimo em responder perguntas sobre física de forma concisa
    e fácil de entender.
    Quando você não sabe a resposta para uma pergunta, você admite
    que não sabe.

    Aqui está uma pergunta: {input}''')

    math_template = ChatPromptTemplate.from_template('''Você é um matemático muito bom.
    Você é ótimo em responder perguntas de matemática.
    Você é tão bom porque consegue decompor
    problemas difíceis em suas partes componentes,
    responder às partes componentes e depois juntá-las
    para responder à pergunta mais ampla.

    Aqui está uma pergunta: {input}''')

    hist_template = ChatPromptTemplate.from_template('''Você é um historiador muito bom.
    Você tem um excelente conhecimento e compreensão de pessoas,
    eventos e contextos de uma variedade de períodos históricos.
    Você tem a capacidade de pensar, refletir, debater, discutir e
    avaliar o passado. Você tem respeito pela evidência histórica
    e a capacidade de usá-la para apoiar suas explicações
    e julgamentos.

    Aqui está uma pergunta: {input}''')

    prompt_infos = [
        {'name': 'Física',
         'description': 'Ideal para responder perguntas sobre física.',
         'prompt_template': phys_template},
        {'name': 'Matemática',
         'description': 'Ideal para responder perguntas sobre matemática.',
         'prompt_template': math_template},
        {'name': 'História',
         'description': 'Ideal para responder perguntas sobre história.',
         'prompt_template': hist_template},
    ]

    destination_chains = {}
    for prompt_info in prompt_infos:
        chain = LLMChain(
            llm=chat,
            prompt=prompt_info['prompt_template'],
            verbose=True,
        )
        destination_chains[prompt_info['name']] = chain

    destinations = [f'{p['name']}: {p['description']}' for p in prompt_infos]
    destinations_str = '\n'.join(destinations)

    router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(destinations=destinations_str)
    router_template = PromptTemplate(
        template=router_template,
        input_variables=['input'],
        output_parser=RouterOutputParser()
    )
    router_chain = LLMRouterChain.from_llm(chat, router_template, verbose=True)

    default_prompt = ChatPromptTemplate.from_template('{input}')
    default_chain = LLMChain(llm=chat, prompt=default_prompt, verbose=True)

    main_chain = MultiPromptChain(
        router_chain=router_chain,
        destination_chains=destination_chains,
        default_chain=default_chain,
        verbose=True,
    )

    response = main_chain.invoke({ 'input': 'O que é um buraco negro?' })
    print(f'Resposta: {response}')

    response = main_chain.invoke({ 'input': 'O que é uma equação quadrática?' })
    print(f'Resposta: {response}')

    response = main_chain.invoke({ 'input': 'Quando foi a revolução industrial?' })
    print(f'Resposta: {response}')
