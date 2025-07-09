import logging
import uvicorn
from fastapi import FastAPI
from config.settings import settings

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
    description="API para meus projetos de AI_AGENTS",
    version="1.0.0"
)

@app.get("/")
async def root():
    logger.info("Endpoint raiz acessado")
    return {"message": "Bem-vindo ao meu projeto de IA!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

if __name__ == "__main__":
    logger.info(f"Inciando servidor em {settings.API_HOST:}:{settings.API_PORT}")
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=int(settings.API_PORT),  # Convertendo para inteiro
        reload=True
    )