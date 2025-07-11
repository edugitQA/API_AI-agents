import logging
import uvicorn
from fastapi import FastAPI
from config.settings import settings
from src.api.routes import router

#logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(settings.LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="API AI_AGENTS",
    description="API com validação de dados e type hints AI_AGENTS",
    version="1.0.1"
)

@app.get("/")
async def root():
    """Rota raiz com as info da API"""
    return {
        "message": "Bem-vindo ao meu projeto de IA!",
        "version": "1.0.1",
        "docs": "/docs",
        "endpoints": {
            "chat": "/api/v1/chat",
            "models": "/api/v1/models",
            "validate_message": "/api/v1/validate-message",
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.1"}



if __name__ == "__main__":
    logger.info(f"Iniciando servidor em {settings.API_HOST}:{settings.API_PORT}")
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=int(settings.API_PORT),  # Convertendo para inteiro
        reload=True
    )