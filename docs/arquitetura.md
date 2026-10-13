# Arquitetura do Projeto — 5 Centavos

## 1. Objetivo

Este documento descreve a organização dos componentes do **5 Centavos** e como eles se comunicam, na arquitetura em camadas adotada na v1.1.0.

---

## 2. Princípios

* Separação de responsabilidades;
* Modularidade e baixo acoplamento;
* Facilidade de manutenção e testabilidade;
* Evolução incremental.

---

## 3. Arquitetura geral

```text
Usuário → Dashboard (Streamlit) → API REST (FastAPI) → Services → Repositories → PostgreSQL
                                              ↓
                                   Analytics & IA (Scikit-learn)
```

Os dados do banco alimentam as camadas de **Analytics e IA**, sempre isolados por `user_id`.

---

## 4. Camadas

### 4.1 Interface
- **Dashboard Streamlit** (`dashboard/`): autenticação, contas, transações, categorias, metas, gráficos Plotly e página de IA;
- **API Docs**: Swagger/OpenAPI gerado automaticamente em `/docs`.

### 4.2 API (`api/`)
- FastAPI com versionamento de rotas em `/api/v1`;
- Autenticação JWT via `HTTPBearer` (dependência `get_current_user`);
- Validação de dados com Pydantic v2;
- Mapeamento de exceções de domínio para HTTP (404/409/422/401) em `api/main.py`;
- Rate limiting (slowapi) nos endpoints sensíveis e logging estruturado (structlog).

### 4.3 Serviços (`services/`) — regras de negócio
- `UserService`: registro (com categorias padrão) e autenticação;
- `AccountService`: CRUD de contas e cálculo de saldo;
- `CategoryService`: CRUD de categorias com unicidade nome+tipo;
- `TransactionService`: CRUD de transações com validação de vínculos e tipos;
- `GoalService`: CRUD de metas e progresso;
- `AnalyticsService`: resumo, indicadores, breakdown por categoria e evolução mensal;
- `services/exceptions.py`: erros de domínio (`NotFoundError`, `ConflictError`, `BusinessRuleError`, `UnauthorizedError`).

### 4.4 Repositórios (`repositories/`) — acesso a dados
- `BaseRepository` genérico (get/create/update/delete);
- `UserRepository`, `AccountRepository`, `CategoryRepository`, `TransactionRepository`, `GoalRepository` — todos com escopo obrigatório por usuário;
- `AnalyticsRepository`: agregações SQL (totais por tipo, por categoria, por mês e por conta).

### 4.5 Persistência (`core/database.py`, `models/`)
- PostgreSQL 16 em produção; SQLite disponível para desenvolvimento/testes;
- **SQLAlchemy 2.0 ORM declarativo** com `Mapped`/`mapped_column`, relacionamentos e integridade (`CHECK`, FK `CASCADE`/`RESTRICT`, `UNIQUE`);
- Valores monetários em `NUMERIC(14,2)` (nunca ponto flutuante);
- Tabelas criadas idempotentemente no startup (`init_db`).

### 4.6 Schemas (`schemas/`)
- Contratos de request/response por domínio;
- Enums compartilhados com os models (`models/enums.py`);
- `from_attributes=True` para serialização ORM;
- Regras básicas na borda (`amount > 0`, tamanhos de texto).

### 4.7 Núcleo (`core/`)
- `config.py`: `pydantic-settings` lendo `.env` (single source de configuração);
- `security.py`: bcrypt + JWT (python-jose);
- `logging.py`: logging estruturado (console em dev, JSON em produção).

---

## 5. Analytics e IA

### Analytics
- Resumo financeiro (receitas, despesas, saldo, taxa de poupança);
- Análise por categoria com percentuais;
- Evolução mensal com saldo acumulado;
- Tudo consolidado em SQL e exposto via `GET /api/v1/analytics/*`.

### IA (`ai/`)
- **TransactionClassifier**: TF-IDF (1–2 gramas) + RandomForest treinado no histórico do próprio usuário;
- **AnomalyDetector**: Isolation Forest sobre valor e dia do mês das despesas;
- **CashFlowPredictor**: médias móveis dos últimos meses por tipo;
- **SpendingClusterer**: K-Means sobre valores de despesa para perfil de consumo;
- **FinancialAdvisor**: orquestrador — treina, gera insights transparentes (fatores explicitados);
- Mínimo de 8 transações do usuário para treino; abaixo disso as respostas são graciosas.

---

## 6. Fluxo de Dados

```text
Usuário → Dashboard → API → Services → Repositories → PostgreSQL
                                          ↓
                 Analytics Repository → AnalyticsService → API → Dashboard
                                          ↓
                 AI Models (Classifier, Detector, Predictor, Clusterer) → Advisor → API → Dashboard
```

---

## 7. Organização do Código

```text
5-Centavos/
├── docs/                          # especificação, requisitos, RN, CU, arquitetura, modelo, DER, roadmap
├── data/                          # CSVs seed para o ETL
├── src/
│   └── cinco_centavos/
│       ├── core/                  # config, database, security, logging
│       ├── models/                # User, Account, Category, Transaction, Goal + enums
│       ├── schemas/               # contratos Pydantic por domínio
│       ├── repositories/          # acesso a dados com escopo por usuário
│       ├── services/              # regras de negócio + exceções
│       ├── api/                   # FastAPI (main, limiter, v1/{deps,router,endpoints})
│       ├── ai/                    # 5 modelos de IA
│       ├── etl/                   # importação CSV idempotente
│       └── dashboard/             # Streamlit (app, api_client, components, pages/)
├── tests/                         # unit / integration / e2e (41 testes)
├── Dockerfile                     # multi-stage, usuário não-root
├── docker-compose.yml             # db + api + dashboard (+ etl profile)
├── entrypoint.sh                  # modos: api | dashboard | etl
├── Makefile
├── pyproject.toml / requirements.txt
└── README.md / CHANGELOG.md
```

---

## 8. Segurança e Testes

* **Segurança:** bcrypt, JWT, isolamento por `user_id`, rate limiting, segredos via `.env` (nunca commitados);
* **Testes:** 41 testes (Pytest) cobrindo regras de negócio, API e jornadas e2e; banco de teste SQLite em memória isolado por teste;
* **Validação:** Pydantic v2 na API + integridade no banco + regras nos serviços.

---

## 9. Deploy e Operação

* **Docker:** multi-stage build (builder/runtime), usuário não-root, venv dedicada em `/opt/venv`;
* **Docker Compose:** `db` (PostgreSQL 16, volume persistido), `api`, `dashboard` e perfil opcional `etl`;
* **Health Checks:** `pg_isready` no banco e `GET /health` na API;
* **Makefile:** `install`, `test`, `run-api`, `run-dashboard`, `run-etl`, `docker-*`;
* **Configuração:** variáveis de ambiente documentadas em `.env.example`.
