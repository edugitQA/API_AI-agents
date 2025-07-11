import time
import functools
from typing import Callable, Any, Dict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def timer(func: Callable) -> Callable:
    """
    Decorator que mede tempo de execução.
    
    Uso:
        @timer
        def minha_funcao():
            # código aqui
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            logger.info(
                f"⏱️ {func.__name__} executada em {execution_time:.4f}s"
            )
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(
                f"❌ {func.__name__} falhou em {execution_time:.4f}s: {e}"
            )
            raise
    
    return wrapper

def retry(max_attempts: int = 3, delay: float = 1.0):
    """
    Decorator que tenta executar função várias vezes.
    Uso:
        @retry(max_attempts=3, delay=2.0)
        def funcao_que_pode_falhar():
            # código aqui
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                    
                except Exception as e:
                    last_exception = e
                    logger.warning(
                        f"🔄 Tentativa {attempt + 1}/{max_attempts} falhou para {func.__name__}: {e}"
                    )
                    
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
                    
            logger.error(f"❌ {func.__name__} falhou após {max_attempts} tentativas")
            raise last_exception
            
        return wrapper
    return decorator

def cache_result(duration_seconds: int = 300):
    """
    Decorator que faz cache de resultados.
    
    Uso:
        @cache_result(duration_seconds=60)
        def funcao_lenta():
            # código aqui
    """
    def decorator(func: Callable) -> Callable:
        cache = {}
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Cria chave única para os parâmetros
            cache_key = str(args) + str(sorted(kwargs.items()))
            current_time = time.time()
            
            # Verifica se tem cache válido
            if cache_key in cache:
                cached_result, cached_time = cache[cache_key]
                if current_time - cached_time < duration_seconds:
                    logger.info(f"📦 Cache hit para {func.__name__}")
                    return cached_result
            
            # Executa função e salva no cache
            result = func(*args, **kwargs)
            cache[cache_key] = (result, current_time)
            
            logger.info(f"💾 Resultado salvo no cache para {func.__name__}")
            return result
            
        return wrapper
    return decorator

def validate_api_key_decorator(func: Callable) -> Callable:
    """
    Decorator que valida API key automaticamente.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Procura API key nos argumentos
        api_key = kwargs.get('api_key') or (args[0] if args else None)
        
        if not api_key or not isinstance(api_key, str):
            raise ValueError("API key é obrigatória")
            
        if len(api_key) < 20:
            raise ValueError("API key inválida - muito curta")
            
        logger.info(f"🔐 API key validada para {func.__name__}")
        return func(*args, **kwargs)
        
    return wrapper

def log_calls(include_args: bool = False):
    """
    Decorator que registra chamadas de funções.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if include_args:
                logger.info(
                    f"📞 [{timestamp}] Chamando {func.__name__} com args={args}, kwargs={kwargs}"
                )
            else:
                logger.info(f"📞 [{timestamp}] Chamando {func.__name__}")
            
            result = func(*args, **kwargs)
            
            logger.info(f"✅ [{timestamp}] {func.__name__} concluída")
            return result
            
        return wrapper
    return decorator
