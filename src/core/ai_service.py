"""
Serviço de IA com decorators aplicados.
É como ter um "assistente super inteligente" com vários superpoderes.
"""

import random
import time
from typing import List, Dict, Any
import logging

from src.utils.decorators import timer, retry, cache_result, validate_api_key_decorator, log_calls
from src.utils.error_handler import InvalidAPIKeyError, ModelNotFoundError, TokenLimitExceededError, AIServiceError
from src.core.data_types import AIrequest, AIResponse, ModelType

logger = logging.getLogger(__name__)

class AIService:
    """
    Serviço principal de IA com decorators.
    É como ter um "cérebro artificial" equipado com ferramentas avançadas.
    """
    
    def __init__(self):
        self.available_models = [model.value for model in ModelType]
        self.max_tokens_per_model = {
            ModelType.OPENAI: 8000,
            ModelType.GEMINI: 32000,
            ModelType.GROK: 100000
        }
    
    @timer
    @retry(max_attempts=3, delay=1.0)
    @log_calls(include_args=False)
    def generate_response(self, request: AIrequest, api_key: str) -> AIResponse:
        """
        Gera resposta usando IA.
        Tem superpoderes: cronômetro, retry automático e logging.
        """
        self._validate_request(request, api_key)
        
        # Simula processamento da IA (depois conectaremos com APIs reais)
        response_text = self._mock_ai_response(request)
        
        return AIResponse(
            response=response_text,
            model_used=request.model.value,
            tokens_used=self._calculate_tokens(request),
            processing_time=random.uniform(0.5, 2.0)
        )
    
    @cache_result(duration_seconds=60)
    @timer
    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """
        Obtém informações sobre um modelo.
        Tem cache de 60 segundos para evitar consultas repetidas.
        """
        if model_name not in self.available_models:
            raise ModelNotFoundError(model_name)
        
        # Simula consulta "lenta" ao banco
        time.sleep(0.5)
        
        return {
            "name": model_name,
            "max_tokens": self.max_tokens_per_model.get(ModelType(model_name), 4000),
            "description": f"Modelo {model_name} para IA generativa",
            "status": "available",
            "pricing": self._get_pricing(model_name)
        }
    
    @validate_api_key_decorator
    @timer
    def validate_api_access(self, api_key: str) -> bool:
        """
        Valida acesso à API.
        Decorator valida automaticamente o formato da API key.
        """
        # Simula validação com serviço externo
        time.sleep(0.2)
        
        # Simula algumas API keys inválidas
        if api_key.endswith("invalid"):
            raise InvalidAPIKeyError("API key foi revogada")
        
        logger.info("✅ API key validada com sucesso")
        return True
    
    def _validate_request(self, request: AIrequest, api_key: str) -> None:
        """Valida requisição internamente"""
        if not api_key:
            raise InvalidAPIKeyError("API key é obrigatória")
        
        if request.model.value not in self.available_models:
            raise ModelNotFoundError(request.model.value)
        
        total_tokens = self._calculate_tokens(request)
        max_tokens = self.max_tokens_per_model.get(request.model, 4000)
        
        if total_tokens > max_tokens:
            raise TokenLimitExceededError(total_tokens, max_tokens)
    
    def _calculate_tokens(self, request: AIrequest) -> int:
        """Calcula tokens da requisição"""
        total_chars = sum(len(msg.content) for msg in request.messages)
        return total_chars // 4  # Estimativa: 4 chars por token
    
    def _mock_ai_response(self, request: AIrequest) -> str:
        """Simula resposta da IA"""
        responses = [
            "Entendi sua pergunta! Aqui está uma resposta detalhada sobre o assunto...",
            "Ótima questão! Vou explicar isso de forma clara e prática...",
            "Baseado no que você perguntou, posso te ajudar com as seguintes informações...",
            "Essa é uma pergunta interessante! Deixe-me quebrar isso em partes..."
        ]
        
        # Simula tempo de processamento
        time.sleep(random.uniform(0.5, 1.5))
        
        return random.choice(responses)
    
    def _get_pricing(self, model_name: str) -> Dict[str, float]:
        """Retorna preços simulados"""
        pricing = {
            ModelType.GPT_3_5: {"input": 0.0015, "output": 0.002},
            ModelType.GPT_4: {"input": 0.03, "output": 0.06},
            ModelType.CLAUDE: {"input": 0.008, "output": 0.024},
            ModelType.GEMINI: {"input": 0.00025, "output": 0.0005}
        }
        
        return pricing.get(ModelType(model_name), {"input": 0.001, "output": 0.002})
