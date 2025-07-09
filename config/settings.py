"""
configurações centralizadas/PAINEL de controle
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """
    centralizar nessa classe todas as configs
    """
    #API
    API_HOST = str = os.getenv("API_HOST", "localhost")
    API_PORT = int = os.getenv("API_PORT", 8000)

    #LLM
    OPENAI_API_KEY = str = os.getenv("OPENAI_API_KEY", "")

    #logs
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")  # type: str
    LOG_FILE = "logs/app.log"

    #CONEXÕES BD
    DATABASE_URL = str = os.getenv("DATABASE_URL", "sqlite:///./app.db")


settings = Settings()