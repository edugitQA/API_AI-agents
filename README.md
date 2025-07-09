# API AI_AGENTS

## Descrição
Este projeto é uma API desenvolvida com FastAPI para gerenciar e integrar agentes de inteligência artificial (AI_AGENTS). A API foi projetada para ser escalável, eficiente e fácil de usar, permitindo que desenvolvedores criem e integrem soluções de IA em seus projetos.

## Funcionalidades
- **Endpoint raiz**: Um ponto de entrada para verificar o funcionamento básico da API.
- **Health Check**: Endpoint para verificar o status da API.
- **Configuração de agentes de IA**: Estrutura para gerenciar agentes de IA.

## Estrutura do Projeto
```
├── main.py                # Arquivo principal para execução da API
├── config/                # Configurações do projeto
│   ├── settings.py        # Configurações gerais (ex.: host, porta, etc.)
├── src/                   # Código-fonte principal
│   ├── api/               # Rotas da API
│   ├── core/              # Lógica central dos agentes de IA
│   ├── utils/             # Funções utilitárias
├── tests/                 # Testes automatizados
├── logs/                  # Arquivos de log
├── requirements.txt       # Dependências do projeto
├── .env                   # Variáveis de ambiente
└── README.md              # Documentação do projeto
```

## Requisitos
- Python 3.12+
- FastAPI
- Uvicorn
- SQLAlchemy
- Psycopg2-binary
- Python-dotenv

## Instalação
1. Clone o repositório:
   ```bash
   git clone https://github.com/edugitQA/API_AI-agents.git
   ```

2. Navegue até o diretório do projeto:
   ```bash
   cd API_AI-agents
   ```

3. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Configuração
Crie um arquivo `.env` com as seguintes variáveis:
```
API_HOST=localhost
API_PORT=8005
OPENAI_API_KEY=sua-chave-aqui
LOG_LEVEL=INFO
DATABASE_URL=sqlite:///./app.db
```

## Executando a API
Execute o seguinte comando para iniciar a API:
```bash
python main.py
```

Acesse os endpoints:
- Endpoint raiz: [http://localhost:8005/](http://localhost:8005/)
- Health Check: [http://localhost:8005/health](http://localhost:8005/health)

## Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença
Este projeto está licenciado sob a [MIT License](https://opensource.org/licenses/MIT).