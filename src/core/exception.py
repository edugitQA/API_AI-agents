class AIServiceError(Exception):
    """Erro base para serviços de IA"""
    def __init__(self, message: str, error_code: str = "AI_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

class InvalidAPIKeyError(AIServiceError):
    """Erro quando API key é inválida"""
    def __init__(self, message: str = "API key inválida"):
        super().__init__(message, "INVALID_API_KEY")

class ModelNotFoundError(AIServiceError):
    """Erro quando modelo não é encontrado"""
    def __init__(self, model_name: str):
        message = f"Modelo '{model_name}' não encontrado"
        super().__init__(message, "MODEL_NOT_FOUND")

class TokenLimitExceededError(AIServiceError):
    """Erro quando ultrapassa limite de tokens"""
    def __init__(self, used_tokens: int, limit: int):
        message = f"Limite de tokens ultrapassado: {used_tokens}/{limit}"
        super().__init__(message, "TOKEN_LIMIT_EXCEEDED")

class RateLimitError(AIServiceError):
    """Erro quando ultrapassa limite de requisições"""
    def __init__(self, message: str = "Limite de requisições ultrapassado"):
        super().__init__(message, "RATE_LIMIT_EXCEEDED")