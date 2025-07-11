# Documentação de Arquitetura do Projeto de IA

## Visão Geral

Este projeto implementa uma API para interação com modelos de IA utilizando FastAPI e Pydantic. A arquitetura segue um padrão modular, com separação clara de responsabilidades entre diferentes componentes.

## Estrutura do Projeto

```
aprendizado/
├── main.py                # Ponto de entrada da aplicação
├── README.md              # Documentação geral
├── requirements.txt       # Dependências do projeto
├── config/                # Configurações centralizadas
│   └── settings.py        # Configurações da aplicação
├── logs/                  # Diretório para armazenamento de logs
│   └── app.log            # Arquivo de log da aplicação
├── src/                   # Código fonte principal
│   ├── api/               # Endpoints da API
│   │   └── routes.py      # Rotas da API
│   ├── core/              # Componentes essenciais
│   │   ├── ai_agent.py    # Implementação de agentes de IA (ainda vazio)
│   │   └── data_types.py  # Modelos de dados e tipos
│   └── utils/             # Utilitários
│       └── helpers.py     # Funções auxiliares
└── tests/                 # Testes automatizados
    └── __init__.py
```

## Componentes Principais

### 1. Modelos de Dados (`src/core/data_types.py`)

Define os tipos de dados e modelos utilizados em toda a aplicação:

- **ModelType (Enum)**: Define os modelos de IA disponíveis (OPENAI, GEMINI, GROK)
- **MessageRole (Enum)**: Define os papéis possíveis para mensagens (USER, SYSTEM, ASSISTANT, TOOL)
- **ChatMessage**: Modelo para mensagens de chat, com validação de conteúdo
- **AIrequest**: Modelo para requisições à IA, incluindo modelo, mensagens, temperatura e tokens
- **AIResponse**: Modelo para respostas da IA, incluindo resposta, modelo utilizado, tokens e tempo de processamento

### 2. API Routes (`src/api/routes.py`)

Implementa os endpoints da API usando FastAPI:

- **POST /api/v1/chat**: Endpoint principal para interação com a IA
- **GET /api/v1/models**: Lista os modelos disponíveis
- **POST /api/v1/validate-message**: Valida uma mensagem antes de enviar para processamento

### 3. Utilitários (`src/utils/helpers.py`)

Funções auxiliares para o funcionamento da aplicação:

- **safe_json_parse**: Análise segura de strings JSON
- **format_response**: Formatação padronizada de respostas da API
- **validate_api_key**: Validação de chaves de API
- **calculate_tokens**: Estimativa do número de tokens em um texto

### 4. Configurações (`config/settings.py`)

Centraliza todas as configurações da aplicação:

- Configurações da API (host, porta)
- Chaves de API para os modelos de IA
- Configurações de log
- Configurações de banco de dados

### 5. Aplicação Principal (`main.py`)

Inicializa a aplicação FastAPI, configura o logging e define rotas básicas:

- **GET /**: Rota raiz com informações sobre a API
- **GET /health**: Verificação de saúde da aplicação

## Fluxo de Funcionamento

1. **Inicialização**:
   - A aplicação é inicializada em `main.py`
   - Configurações são carregadas de variáveis de ambiente via `settings.py`
   - O sistema de logging é configurado
   - O servidor FastAPI é iniciado

2. **Processamento de Requisições**:
   - O cliente envia uma requisição para o endpoint `/api/v1/chat`
   - A requisição é validada usando os modelos Pydantic (`AIrequest`)
   - Os dados são processados (atualmente uma simulação)
   - Uma resposta é formatada e retornada seguindo o modelo `AIResponse`

3. **Validação e Formatação**:
   - As mensagens são validadas usando o modelo `ChatMessage`
   - As respostas são formatadas usando a função `format_response`
   - Os tokens são calculados usando a função `calculate_tokens`

## Estado Atual do Desenvolvimento

O projeto está em fase inicial de desenvolvimento. A estrutura básica está implementada, incluindo:

- Definição de modelos de dados com validação
- Rotas da API com simulação de processamento
- Sistema de logging
- Configuração centralizada

O componente `ai_agent.py` ainda está vazio, indicando que a integração real com modelos de IA ainda não foi implementada.

## Próximos Passos Sugeridos

1. Implementar a integração real com os modelos de IA (OpenAI, Gemini, Grok)
2. Adicionar autenticação e autorização para os endpoints
3. Implementar armazenamento de conversas
4. Desenvolver testes automatizados
5. Adicionar documentação detalhada para a API
6. Implementar monitoramento de uso e limites de tokens

Esta arquitetura fornece uma base sólida para a construção de um sistema de interação com modelos de IA, com ênfase em validação de dados, tratamento de erros e modularidade.
