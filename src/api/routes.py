from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import logging
from src.core.data_types import ModelType
from src.core.data_types import AIrequest, AIResponse, ChatMessage, MessageRole
from src.utils.helpers import format_response, validate_api_key, calculate_tokens

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["AI"])

@router.post("/chat", response_model=AIResponse)
async def chat_with_ai(request:AIrequest):
    """
    Endpoint para interagir com a IA.
    
    Args:
        request: Dados da conversa(já validados pelo Pydantic).
    
    Returns:
        return: Resposta da IA formatada.
    """
    logger.info(f"Recebida requisição para modelo {request.model}")

#simulação previa de processamento
    try:
        total_tokens = sum(calculate_tokens(msg.content) for msg in request.messages)
        response_content = f"OLá! Recebi {len(request.messages)} mensagens usando {total_tokens} tokens."

        #REPOSTA PADRONIZADA
        ai_response = AIResponse(
            response=response_content,
            model_used=request.model,
            tokens_used=total_tokens,
            processing_time=0.5  # Simulação de tempo de processamento
        )
        logger.info(f"Resposta gerada com sucesso usando o modelo {request.model}")
        return ai_response
    except Exception as e:
        logger.error(f"Erro ao processar a requisição: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor ao processar a requisição")



@router.get("/models")
async def list_models():
    """
    Lista modelos disponíveis.
    É como um "catálogo" dos modelos de IA que temos.
    """
    
    
    models = [
        {
            "name": model.value,
            "display_name": model.value.replace("-", " ").title(),
            "recommended_for": get_model_recommendation(model)
        }
        for model in ModelType
    ]
    
    return format_response("Modelos disponíveis", {"models": models})

@router.post("/validate-messagem")
async def validate_message(content: str = Query(..., min_length=1)):
    """
    valida msg antes de enviar
    """
    try:
        message = ChatMessage(role=MessageRole.USER, content=content)
        tokens = calculate_tokens(content)
        word_count = len(content.split())

        validate_result ={
            "is_valid": True,
            "tokens_estimated": tokens,
            "word_count": word_count,
            "character_count": len(content),
            "message": "Mensagem válida!"
        }
        return format_response("Mensagem validada com sucesso", validate_result)
    except Exception as e:
        logger.error(f"Erro ao validar mensagem: {e}")
        return format_response(
            "Erro na validação",
            {"is_valid": False, "error": str(e)},
        )

def get_model_recommendation(model) -> str:
    """
    Retorna recomendação de uso para cada modelo.
    É como um "guia de uso" personalizado.
    """
    recommendations = {
        "openai": "Conversas rápidas e tarefas simples",
        "gemini": "Análises complexas e raciocínio avançado",
        "grok": "Análise de documentos e escrita criativa",
    }
    return recommendations.get(model.value, "Uso geral")


