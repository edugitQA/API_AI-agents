# Definições de exceções customizadas
class AIServiceError(Exception):
    def __init__(self, error_code: str, message: str):
        self.error_code = error_code
        self.message = message

class InvalidAPIKeyError(AIServiceError):
    pass
class ModelNotFoundError(AIServiceError):
    pass
class RateLimitError(AIServiceError):
    pass
class TokenLimitExceededError(AIServiceError):
    pass

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
import logging
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)

async def global_exception_handler(request: Request, exc: Exception):
    """
    Tratador global de exceções.
    É como um "para-raios" que captura todos os erros não tratados.
    """
    logger.error(f"Erro não tratado: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Erro interno do servidor",
            "message": "Algo deu errado. Nossa equipe foi notificada.",
            "timestamp": datetime.now().isoformat()
        }
    )

async def ai_service_exception_handler(request: Request, exc: AIServiceError):
    """
    Tratador específico para erros de IA.
    É como um "especialista" que entende erros específicos da IA.
    """
    status_code = 400
    
    # Mapeia tipos de erro para códigos HTTP
    if isinstance(exc, InvalidAPIKeyError):
        status_code = 401
    elif isinstance(exc, ModelNotFoundError):
        status_code = 404
    elif isinstance(exc, RateLimitError):
        status_code = 429
    elif isinstance(exc, TokenLimitExceededError):
        status_code = 413
    
    logger.error(f"Erro de IA: {exc.error_code} - {exc.message}")
    
    return JSONResponse(
        status_code=status_code,
        content={
            "error": exc.error_code,
            "message": exc.message,
            "timestamp": datetime.now().isoformat()
        }
    )

def handle_validation_error(errors: list) -> Dict[str, Any]:
    """
    Trata erros de validação do Pydantic.
    É como um "corretor" que explica exatamente o que está errado.
    """
    formatted_errors = []
    
    for error in errors:
        formatted_errors.append({
            "field": " -> ".join(str(x) for x in error["loc"]),
            "message": error["msg"],
            "invalid_value": error.get("input", "N/A")
        })
    
    return {
        "error": "VALIDATION_ERROR",
        "message": "Dados inválidos fornecidos",
        "details": formatted_errors,
        "timestamp": datetime.now().isoformat()
    }