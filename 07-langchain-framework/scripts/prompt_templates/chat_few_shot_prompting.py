from langchain.prompts.few_shot import FewShotChatMessagePromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain_openai.chat_models import ChatOpenAI

examples = [
    {"question": "Quem viveu mais tempo, Muhammad Ali ou Alan Turing?",
     "response":
     """São necessárias perguntas de acompanhamento aqui: Sim.
Pergunta de acompanhamento: Quantos anos Muhammad Ali tinha quando morreu?
Resposta intermediária: Muhammad Ali tinha 74 anos quando morreu.
Pergunta de acompanhamento: Quantos anos Alan Turing tinha quando morreu?
Resposta intermediária: Alan Turing tinha 41 anos quando morreu.
Então a resposta final é: Muhammad Ali
""",
    },
    {"question": "Quando nasceu o fundador do craigslist?",
     "response":
"""São necessárias perguntas de acompanhamento aqui: Sim.
Pergunta de acompanhamento: Quem foi o fundador do craigslist?
Resposta intermediária: O craigslist foi fundado por Craig Newmark.
Pergunta de acompanhamento: Quando nasceu Craig Newmark?
Resposta intermediária: Craig Newmark nasceu em 6 de dezembro de 1952.
Então a resposta final é: 6 de dezembro de 1952
""",
    },
    {"question": "Quem foi o avô materno de George Washington?",
     "response":
"""São necessárias perguntas de acompanhamento aqui: Sim.
Pergunta de acompanhamento: Quem foi a mãe de George Washington?
Resposta intermediária: A mãe de George Washington foi Mary Ball Washington.
Pergunta de acompanhamento: Quem foi o pai de Mary Ball Washington?
Resposta intermediária: O pai de Mary Ball Washington foi Joseph Ball.
Então a resposta final é: Joseph Ball
""",
    },
    {"question": "Os diretores de Jaws e Casino Royale são do mesmo país?",
     "response":
"""São necessárias perguntas de acompanhamento aqui: Sim.
Pergunta de acompanhamento: Quem é o diretor de Jaws?
Resposta Intermediária: O diretor de Jaws é Steven Spielberg.
Pergunta de acompanhamento: De onde é Steven Spielberg?
Resposta Intermediária: Estados Unidos.
Pergunta de acompanhamento: Quem é o diretor de Casino Royale?
Resposta Intermediária: O diretor de Casino Royale é Martin Campbell.
Pergunta de acompanhamento: De onde é Martin Campbell?
Resposta Intermediária: Nova Zelândia.
Então a resposta final é: Não
""",
    },
]

def execute():
    example_prompt = ChatPromptTemplate(
        [
            ('human', '{question}'),
            ('ai', '{response}')
        ]
    )
    example_prompt.format(**examples[0])
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
    )
    prompt = ChatPromptTemplate(
        [
            few_shot_prompt,
            ('human', '{input}')
        ]
    )
    prompt_with_values = prompt.format(input='Quem fez mais gols, Romário  ou Pelé?')
    # print(prompt_with_values)

    chat = ChatOpenAI()
    response = chat.invoke(prompt_with_values)
    print(f'Resposta: {response}')
