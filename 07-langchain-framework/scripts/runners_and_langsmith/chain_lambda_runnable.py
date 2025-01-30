from langchain_core.runnables import RunnableLambda

def say_hello(person):
    return f'Hello, {person['name']}!'

def execute():
    # Transform custom function in an runner

    runnable_say_hello = RunnableLambda(say_hello)

    response = runnable_say_hello.invoke({ 'name': 'John Doe' })

    print(f'Resposta: {response}')
