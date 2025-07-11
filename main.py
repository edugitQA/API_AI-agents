import logging
import uvicorn
from fastapi import FastAPI
from config.settings import settings
from src.api.routes import router
from datetime import datetime
from contextlib import asynccontextmanager

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

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Iniciando API IA com Decorators...")
    logger.info("✅ Todos os sistemas operacionais!")
    yield
    logger.info("🛑 Encerrando API IA...")
    logger.info("✅ Shutdown realizado com sucesso!")

app = FastAPI(
    title="API AI_AGENTS",
    description="API com validação de dados e type hints AI_AGENTS",
    version="1.0.1",
    lifespan=lifespan
)

app.include_router(router)

@app.get("/")
async def root():
    """Rota raiz com informações da API"""
    return {
        "message": "API IA com Superpoderes! 🦸‍♂️",
        "version": "2.0.0",
        "features": [
            "⏱️ Cronômetro automático",
            "🔄 Retry inteligente",
            "📦 Cache de resultados",
            "🛡️ Tratamento de erros",
            "📊 Logging detalhado"
        ],
        "endpoints": {
            "docs": "/docs",
            "chat": "/api/v1/chat",
            "models": "/api/v1/models/{model_name}",
            "validate": "/api/v1/validate-key"
        }
    }

@app.get("/health")
async def health_check():
    """
    Health check avançado com informações detalhadas.
    É como um "checkup médico" completo da sua API.
    """
    import psutil
    import os
    
    return {
        "status": "healthy",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat(),
        "system": {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent
        },
        "process": {
            "pid": os.getpid(),
            "memory_mb": psutil.Process().memory_info().rss / 1024 / 1024
        }
    }

if __name__ == "__main__":
    logger.info(f"Iniciando servidor em {settings.API_HOST}:{settings.API_PORT}")
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True,
        log_level=settings.LOG_LEVEL.lower()
    )