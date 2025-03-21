from langchain_core.utils.function_calling import convert_to_openai_function
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class QueryType(str, Enum):
    all = 'all'
    unread = 'unread'
    reat = 'read'

class GetEmails(BaseModel):
    """Recuperar emails com filtros de lidos e/ou não lidos"""
    type: str = Field(description='Tipo de filtro dos emails')[QueryType]
    quantity: Optional[int] = 10

def execute():
    tool = convert_to_openai_function(GetEmails)
    print(f'===> Tool: {tool}')
