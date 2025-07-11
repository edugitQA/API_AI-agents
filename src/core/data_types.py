#tipos de dados e modelos de para IA
from typing import List, Annotated, Optional, Union, Any
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from enum import Enum

class ModelType (str, Enum):
    """Enum para modelos de llm"""
    OPENAI = "gpt-4o" 
    GEMINI = "gemini-2-5-flash"
    GROK = "llama-3-3-70b-versatile"

class MessageRole(str, Enum):
    """definir papeis possiveis pra uma mensagem com IA"""
    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"
    TOOL = "tool"

class ChatMessage(BaseModel):
    """Modelo de mensagem voltado pra chat"""
    role: MessageRole
    content: str = Field(..., min_length=1, max_length=10000)
    timestamp: datetime = Field(default_factory=datetime.now)

    @field_validator('content')
    def validate_content(cls, v):
        """Valida se conteudo não é só espaço em branco"""
        if not v.strip():
            raise ValueError("Conteudo nao pode estar vazio")
        return v.strip()
    
class AIrequest(BaseModel):
    """Modelo de requisicao para a IA"""
    model: ModelType  # Corrigido para usar o Enum completo
    messages: List[ChatMessage]
    temperature: float = Field(0.7, ge=0.0, le=1.0)
    max_tokens: Optional[int] = Field(None, ge=1, le=4000)

    class Config:
        schema_extra = {
        "example": {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": "Qual é a capital do brasil?"
                }
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }   
    }

class AIResponse(BaseModel):
    """Modelo de resposta da IA"""
    response: str
    model_used: str
    tokens_used: int
    processing_time: float
    timestamp: datetime = Field(default_factory=datetime.now)

