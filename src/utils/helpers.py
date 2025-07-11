import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)

def safe_json_parse(json_string: str) -> Optional[Dict[str, Any]]:
    """
    Tentar converter JSON em dicionario de forma segura.

    Args:
        json_string (str): A string no formato JSON.
    
    Returns:
        dicionario com dados ou none no caso se erro.
    """
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao analisar JSON: {e}")
        return None

def format_response(content: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Formatar a resposta padrão da API.
    Args:
        content (str): Conteúdo principal.
        metadata : dados adicionais (opcionais).
    Returns:
        dicionario formatado.
    """
    response = {
        "content": content,
        "timestamp": datetime.now().isoformat(),  
        "sucess": True 
    }

    if metadata:
        response["metadata"] = metadata
    return response

def validate_api_key(api_key: str) -> bool:
    """
    Valida se API tem formato valido.

    Args:
        api_key: Chave api pra validar.
    Returns:
        True se valida, False se contratio.
    
    """
    if not api_key:
        return False
    if len(api_key) < 20:
        return False
    if not api_key.startswith(("sk-", "pk-", "gsk-")):
        logger.error("Chave API deve começar com 'sk-', 'pk-' ou 'gsk-'")
        return False
    return True

def calculate_tokens(text: str) -> int:
    """
    Estima número de tokens em um texto.
   
    Args:
        text: Texto para contar tokens
        
    Returns:
        Número estimado de tokens
    """
# Estimativa simples: ~4 caracteres por token
    return len(text) // 4



if __name__ == "__main__":
    # Exemplo 1: Usando safe_json_parse
    json_string = '{"name": "John", "age": 30}'
    parsed_data = safe_json_parse(json_string)
    if parsed_data:
        print("JSON analisado com sucesso:", parsed_data)
    else:
        print("Erro ao analisar JSON.")

    # Exemplo 2: Usando o format_response
    response = format_response(
        content="Operação realizada com sucesso!",
        metadata={"user_id": 123, "operation": "create"}
    )
    print("Resposta formatada:", response)

    # Exemplo 3: Usando o validate_api_key
    api_key = "-123456766666"
    is_valid = validate_api_key(api_key)
    print(f"A chave API '{api_key}' é válida? {is_valid}")

    # Exemplo 4: Usando o calculate_tokens
    text = "quem nasceu primeiro ovo ou a galinha?."
    tokens = calculate_tokens(text)
    print(f"Número estimado de tokens: {tokens}")

    