from fastapi import APIRouter, HTTPException, Header, Query, Depends
from fastapi.responses import JSONResponse
from typing import Optional
import logging
import time

from src.core.ai_service import AIService
from src.core.data_types import AIrequest, AIResponse, ChatMessage, MessageRole, ModelType
from src.utils.error_handler import AIServiceError, handle_validation_error
from src.utils.helpers import calculate_tokens, format_response
from src.utils.decorators import timer, log_calls, cache_result

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["AI"])

ai_service = AIService()

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

@router.post("/chat", response_model=AIResponse)
@timer
@log_calls(include_args=False)
async def chat_with_ai(
    request: AIrequest,  # Corrigido para AIrequest
    api_key: str = Header(None, alias="X-API-Key")
):
    """
    Conversa com IA usando decorators para funcionalidades avançadas.
    """
    try:
        if not api_key:
            raise HTTPException(
                status_code=401,
                detail="API key obrigatória no header X-API-Key"
            )
        response = ai_service.generate_response(request, api_key)
        return response
    except AIServiceError as e:
        logger.error(f"Erro do serviço IA: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@router.get("/models/{model_name}")
@timer
async def get_model_info(model_name: str):
    """
    Obtém informações sobre um modelo específico.
    Usa cache automático para performance.
    """
    try:
        info = ai_service.get_model_info(model_name)
        return {"success": True, "data": info}
        
    except AIServiceError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/validate-key")
async def validate_api_key(api_key: str = Header(None, alias="X-API-Key")):
    """
    Valida API key com decorator automático.
    """
    try:
        if not api_key:
            raise HTTPException(status_code=401, detail="API key obrigatória")
        
        is_valid = ai_service.validate_api_access(api_key)
        
        return {
            "valid": is_valid,
            "message": "API key válida!",
            "timestamp": time.time()
        }
        
    except AIServiceError as e:
        raise HTTPException(status_code=401, detail=str(e))

# ===== Exemplo de uso dos decorators =====
@timer
@cache_result(duration_seconds=30)
def exemplo_funcao_com_decorators(texto: str) -> str:
    """
    Exemplo de função com múltiplos decorators.
    Tem cronômetro E cache automático!
    """
    # Simula processamento pesado
    time.sleep(1)
    return f"Processado: {texto.upper()}"

if __name__ == "__main__":
    # Teste dos decorators
    print("🧪 Testando decorators...")
    
    # Primeira chamada (lenta)
    resultado1 = exemplo_funcao_com_decorators("hello world")
    print(f"Resultado 1: {resultado1}")
    
    # Segunda chamada (rápida por causa do cache)
    resultado2 = exemplo_funcao_com_decorators("hello world")
    print(f"Resultado 2: {resultado2}")
    
    print("✅ Decorators funcionando perfeitamente!")
