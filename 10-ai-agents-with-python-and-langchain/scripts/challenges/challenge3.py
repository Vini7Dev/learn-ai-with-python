import smtplib
import ssl
import os

from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain_openai.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_core.agents import AgentFinish
from langchain.agents import tool
from pydantic import BaseModel, Field
from email.message import EmailMessage

class SendEmailArgs(BaseModel):
    recipient: str = Field(description='Email do destinatário')
    title: str = Field(description='Título do email')
    body: str = Field(description='Conteúdo da mensagem do email')

@tool
def send_email(recipient, title, body):
    '''Função responsável por enviar um email'''

    print(f'Recipient: {recipient}')
    print(f'Title: {title}')
    print(f'Body: {body}')

    user_email = os.getenv('SENDER_EMAIL')
    app_key = os.getenv('EMAIL_API_KEY')
    message_email = EmailMessage()
    message_email['From'] = user_email
    message_email['To'] = recipient
    message_email['Subject'] = title

    message_email.set_content(body)
    safe = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=safe) as smtp:
        smtp.login(user_email, app_key)
        smtp.sendmail(user_email, recipient, message_email.as_string())

tools = [send_email]
tools_json = [convert_to_openai_function(tool) for tool in tools]
tool_run = { tool.name: tool for tool in tools }

def routing(result):
    if isinstance(result, AgentFinish):
        return result.return_values['output']
    else:
        return tool_run[result.tool].run(result.tool_input)

def execute():
    prompt = ChatPromptTemplate.from_messages([
        ('system', 'Você é um assistente amigável chamado Vinícius.'),
        ('user', '{input}'),
    ])

    chat = ChatOpenAI(model='gpt-3.5-turbo-0125')

    chain = prompt | chat.bind(functions=tools_json) | OpenAIFunctionsAgentOutputParser() | routing

    result = chain.invoke({ 'input': 'Envie um email para a "jane@mail.com" com o título "Bom dia!" e a mensagem "Tudo bem com você?".' })

    print(f'Resultado: {result}')
