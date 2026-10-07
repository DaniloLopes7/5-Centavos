# Changelog — 5 Centavos

Todas as mudanças notáveis deste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

---

## [1.0.0] - 2024-10-07

### Adicionado
- **Docker & Deploy (v1.0.0)**
  - Dockerfile multi-stage otimizado (builder + runtime)
  - docker-compose.yml com PostgreSQL, API, Dashboard, ETL opcional
  - Health checks para PostgreSQL (pg_isready) e API (/health)
  - Usuário não-root no container
  - Volumes persistentes para dados do PostgreSQL
  - Makefile com comandos: install, test, run-api, run-dashboard, run-etl, docker-build, docker-up, docker-down, docker-logs, clean, lint, format
  - .dockerignore para build otimizado
  - .env.example para configuração

### Alterado
- Atualização de todas documentações para v1.0.0
- README completo com instruções Docker e desenvolvimento local
- Roadmap com todas versões concluídas
- Requisitos marcados como implementados

---

## [0.8.0] - 2024-10-07

### Adicionado
- **Inteligência Artificial (v0.8.0)**
  - `src/ai/__init__.py` com 5 modelos de ML:
    - `TransactionClassifier`: RandomForest para classificação automática de categorias
    - `AnomalyDetector`: Isolation Forest para detecção de gastos anômalos
    - `CashFlowPredictor`: Previsão de fluxo de caixa (médias móveis)
    - `SpendingClusterer`: K-Means para perfis de comportamento (Conservador/Equilibrado/Gastador)
    - `FinancialAdvisor`: Orquestrador que combina todos os modelos
  - `FinancialAdvisor.train_all()`: Treina todos modelos com dados do usuário
  - `FinancialAdvisor.get_insights()`: Retorna insights, previsões e anomalias
  - Endpoints IA em `/api/v1/ai/`:
    - `POST /ai/train` - Treina todos modelos
    - `POST /ai/predict-category` - Prediz categoria da transação
    - `GET /ai/insights` - Insights + previsões + anomalias
    - `GET /ai/cashflow-prediction` - Previsão fluxo de caixa (3 meses)
    - `GET /ai/anomalies` - Transações anômalas detectadas
    - `GET /ai/spending-profile` - Perfil de gasto do usuário

### Alterado
- Atualização `src/api/v1/router.py` para incluir endpoints IA
- `requirements.txt` com scikit-learn, joblib, scipy

---

## [0.7.0] - 2024-10-07

### Adicionado
- **Dashboard Streamlit (v0.7.0)**
  - `src/dashboard/app.py` - Aplicação Streamlit completa
  - 6 páginas navegáveis via sidebar:
    - 📈 Dashboard (resumo + gráficos pizza/barras/linhas)
    - 🏦 Contas (CRUD + saldo em tempo real)
    - 💳 Transações (CRUD + filtros + extrato formatado)
    - 🏷️ Categorias (separadas Receita/Despesa)
    - 🎯 Metas (progresso visual + adicionar progresso)
    - 📊 Analytics (indicadores + gráficos detalhados + tendências)
  - Gráficos Plotly interativos:
    - Pizza: distribuição de despesas por categoria
    - Barras agrupadas: receitas vs despesas mensais
    - Linhas: evolução com médias móveis (3 meses)
    - Scatter: tendências com hover unificado
  - Autenticação via JWT integrada
  - Comunicação com API via HTTP (requests)
  - Sidebar com navegação e logout
  - Formulários validados para todas operações CRUD

### Adicionado
- Dependências: streamlit, plotly, requests
- `API_BASE_URL` configurável via env

---

## [0.6.0] - 2024-10-07

### Adicionado
- **Analytics (v0.6.0)**
  - `AnalyticsRepository`: Consultas SQL para indicadores
    - Resumo financeiro (receitas, despesas, saldo, contas, transações)
    - Resumo por categoria (com percentuais)
    - Evolução mensal (últimos 12 meses)
  - `AnalyticsService`: Camada de serviço para analytics
  - Endpoints `/api/v1/analytics/`:
    - `GET /analytics/summary` - Resumo financeiro + taxa poupança
    - `GET /analytics/categories` - Por categoria (receitas/despesas)
    - `GET /analytics/monthly` - Evolução mensal (12 meses)
  - Integração no Dashboard (página Analytics)

---

## [0.5.0] - 2024-10-07

### Adicionado
- **API REST FastAPI (v0.5.0)**
  - `src/api/main.py`: App FastAPI com lifespan, CORS, health check
  - `src/api/v1/router.py`: Router principal com prefixo `/api/v1`
  - `src/api/v1/deps.py`: Dependências (JWT auth, get_current_user)
  - `src/api/v1/schemas.py`: Pydantic models (User, Account, Category, Transaction, Goal, Analytics)
  - Endpoints organizados por domínio:
    - **Auth** (`/auth`): register, login, me
    - **Users** (`/users/me`): accounts, categories CRUD
    - **Transactions** (`/transactions`): CRUD + filtro por conta
    - **Goals** (`/goals`): CRUD + progresso
    - **Analytics** (`/analytics`): summary, categories, monthly
  - Autenticação JWT (python-jose):
    - Access tokens com expiração configurável
    - Dependency `get_current_user` para proteção de rotas
    - OAuth2PasswordRequestForm para login Swagger
  - Documentação automática OpenAPI/Swagger em `/docs`
  - Health check em `/health`

### Alterado
- `src/cinco_centavos/database.py`: Migração completa para PostgreSQL
  - `DATABASE_URL` via .env
  - `CURRENT_TIMESTAMP` em vez de `datetime('now')`
  - `information_schema.tables` em vez de `sqlite_master`
  - `SERIAL` em vez de `AUTOINCREMENT`
  - `TIMESTAMP` em vez de `DATETIME`
- `src/etl/load_data.py`: Schema PostgreSQL (SERIAL, TIMESTAMP, FKs)
- `requirements.txt`: fastapi, uvicorn, pydantic, python-jose, python-multipart, email-validator, httpx

---

## [0.4.0] - 2024-10-07

### Adicionado
- **PostgreSQL + Arquitetura em Camadas (v0.4.0)**
  - Migração completa SQLite → PostgreSQL
  - Arquitetura em camadas implementada:
    - `src/services/`: UserService, AccountService, CategoryService, TransactionService, GoalService, AnalyticsService
    - `src/repositories/`: UserRepository, AccountRepository, CategoryRepository, TransactionRepository, GoalRepository, AnalyticsRepository
    - `src/schemas/`: Pydantic models para validação
  - SQLAlchemy Core (Engine, text(), transações com context managers)
  - Connection pooling automático
  - Testes automatizados com Pytest (6 testes passando):
    - test_password_security
    - test_user_lifecycle
    - test_account_management
    - test_category_management
    - test_transaction_and_balance
    - test_goal_management

### Alterado
- `src/cinco_centavos/database.py`: Engine PostgreSQL via `DATABASE_URL`
- `src/etl/load_data.py`: Schema PostgreSQL (SERIAL, TIMESTAMP, FKs, DROP/CREATE)
- `data/usuarios.csv`: Senhas bcrypt válidas para testes
- `requirements.txt`: psycopg2-binary, python-dotenv, pytest

---

## [0.3.0] - 2024-10-07

### Adicionado
- **Sistema Financeiro + SQLite (v0.3.0)**
  - CLI funcional (`src/cinco_centavos/main.py`):
    - Menu principal, login, cadastro
    - Menu contas: extrato, transações, metas, nova conta, nova categoria
  - `src/cinco_centavos/database.py`: SQLite + SQLAlchemy
    - CRUD completo: users, accounts, categories, transactions, goals
    - Hash de senhas (bcrypt), categorias padrão
  - ETL (`src/etl/load_data.py`):
    - Criação de tabelas SQLite
    - Carga de CSVs iniciais (usuarios, contas, categorias, metas, transações)
  - Dados de exemplo em `data/`:
    - usuarios.csv, contas.csv, categorias.csv, metas.csv, transacoes.csv
  - Estrutura inicial: `src/cinco_centavos/`, `src/etl/`, `tests/`, `data/`, `docs/`

---

## [0.2.0] - 2024-10-07

### Adicionado
- **Estrutura Inicial Python (v0.2.0)**
  - Configuração do ambiente Python
  - Estrutura de pastas: `src/`, `tests/`, `data/`, `docs/`
  - `requirements.txt` inicial
  - `.gitignore`, `LICENSE`, `README.md`

---

## [0.1.0] - 2024-10-07

### Adicionado
- **Planejamento e Documentação (v0.1.0)**
  - Documentação completa em `docs/`:
    - `especificacao.md`: Especificação técnica
    - `requisitos.md`: Requisitos funcionais e não-funcionais
    - `regras-de-negocio.md`: Regras de negócio
    - `casos-de-uso.md`: Casos de uso
    - `modelo-de-dados.md`: Modelo de dados
    - `DER.md`: Diagrama Entidade-Relacionamento (Mermaid)
    - `arquitetura.md`: Arquitetura do sistema
    - `roadmap.md`: Roadmap de versões
  - `README.md` inicial
  - `LICENSE` (MIT)
  - `.gitignore`

---

## Versões Anteriores (Histórico)

### [0.0.1] - 2023-09-09
- Commit inicial: `da2d246 Initial commit`
- Estrutura base do repositório