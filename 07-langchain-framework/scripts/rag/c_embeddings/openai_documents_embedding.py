import numpy as np
from langchain_openai.embeddings import OpenAIEmbeddings

def execute():
    embedding_model = OpenAIEmbeddings(model='text-embedding-ada-002')

    question = 'O que é um cachorro?'

    question_embedding = embedding_model.embed_query(question)

    print(f'QUESTION > Len: {len(question_embedding)} | Max: {max(question_embedding)} | Min: {min(question_embedding)}')

    embeddings = embedding_model.embed_documents([
        'Eu gosto de cachorros',
        'Eu gosto de animais',
        'O tempo está ruim lá fora',
    ])

    for embedding in embeddings:
        print(f'Len: {len(embedding)} | Max: {max(embedding)} | Min: {min(embedding)}')

    semantic1 = np.dot(embeddings[0], embeddings[1])
    semantic2 = np.dot(embeddings[0], embeddings[2])
    semantic3 = np.dot(embeddings[1], embeddings[2])
    print(f'Semântica 1: {semantic1} | Semântica 2: {semantic2} | Semântica 3: {semantic3}')

    for i in range(len(embeddings)):
        for j in range(len(embeddings)):
            print(round(np.dot(embeddings[i], embeddings[j]), 2), end=' | ')
        print()
