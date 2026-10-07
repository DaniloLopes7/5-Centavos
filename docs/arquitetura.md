# Arquitetura do Projeto — 5 Centavos

## 1. Objetivo

Este documento descreve a organização dos componentes do **5 Centavos** e como eles se comunicam, permitindo a evolução gradual do projeto.

---

## 2. Princípios

* Separação de responsabilidades;
* Modularidade e baixo acoplamento;
* Facilidade de manutenção e testabilidade;
* Evolução incremental.

---

## 3. Arquitetura geral

```text
Usuário → Interface/UI (Streamlit/CLI) → API (FastAPI) → Services → Repositories → Database (PostgreSQL)
                                              ↓
                                    Analytics & AI (Scikit-learn)
```

Os dados do banco alimentam as camadas de **Analytics e IA**.

---

## 4. Camadas

### 4.1 Interface
Responsável pela interação com o usuário:
- **Streamlit Dashboard**: Dashboard interativo com gráficos Plotly
- **CLI**: Interface de linha de comando (main.py)
- **API Docs**: Swagger/OpenAPI em /docs

### 4.2 API (FastAPI)
Disponibiliza os recursos do sistema via REST:
- Autenticação JWT (python-jose)
- Validação de dados com Pydantic
- Documentação automática OpenAPI/Swagger
- Endpoints organizados por domínio (auth, users, transactions, goals, analytics, ai)

### 4.3 Camada de Serviços (`src/services/`)
Contém as regras de negócio:
- `UserService`: Autenticação, registro, categorias padrão
- `AccountService`: CRUD contas, cálculo de saldo
- `CategoryService`: CRUD categorias
- `TransactionService`: CRUD transações, validação tipo categoria
- `GoalService`: CRUD metas, progresso
- `AnalyticsService`: Resumos, indicadores, análises

### 4.4 Camada de Repositórios (`src/repositories/`)
Abstração de acesso a dados:
- `UserRepository`, `AccountRepository`, `CategoryRepository`
- `TransactionRepository`, `GoalRepository`, `AnalyticsRepository`
- Usam SQLAlchemy Core com queries SQL parametrizadas

### 4.5 Camada de Persistência
- **PostgreSQL 16** como banco principal
- **SQLAlchemy 2.0** Core (Engine, Text queries)
- Connection pooling e transações via context managers
- Migração de SQLite para PostgreSQL concluída (v0.4.0)

### 4.6 Schemas (`src/schemas/`)
Validação e serialização com Pydantic v2:
- Models de request/response
- Enums para tipos controlados
- Configuração `from_attributes=True` para ORM

---

## 5. Analytics e IA

### Analytics (`src/services/AnalyticsService`, `src/repositories/AnalyticsRepository`)
- Resumo financeiro (receitas, despesas, saldo, taxa de poupança)
- Análise por categoria (receitas/despesas)
- Evolução mensal com médias móveis
- Indicadores: total receitas, total despesas, saldo, contas, transações

### IA (`src/ai/`)
- **TransactionClassifier**: RandomForest para classificação automática de categorias
- **AnomalyDetector**: Isolation Forest para detecção de gastos anômalos
- **CashFlowPredictor**: Previsão de fluxo de caixa baseada em médias móveis
- **SpendingClusterer**: K-Means para perfis de comportamento financeiro
- **FinancialAdvisor**: Orquestrador que combina todos os modelos

---

## 6. Fluxo de Dados

```text
Usuário → Interface (Streamlit/CLI) → API (FastAPI) 
    → Services (Regras de Negócio) → Repositories (Acesso a Dados) 
    → PostgreSQL
    ↓
Analytics Repository → Analytics Service → API → Dashboard
    ↓
AI Models (Classifier, AnomalyDetector, Predictor) → Insights → API → Dashboard
```

---

## 7. Organização do Código (Implementado)

```text
5-Centavos/
├── docs/
├── src/
│   ├── api/
│   │   ├── main.py
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py
│   │       │   ├── users.py
│   │       │   ├── transactions.py
│   │       │   ├── goals.py
│   │       │   ├── analytics.py
│   │       │   └── ai.py
│   │       ├── deps.py
│   │       └── router.py
│   ├── dashboard/
│   │   └── app.py
│   ├── ai/
│   │   └── __init__.py
│   ├── analytics/
│   ├── services/
│   ├── repositories/
│   ├── schemas/
│   ├── etl/
│   └── cinco_centavos/
│       ├── main.py
│       └── database.py
│
├── tests/
├── data/
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── requirements.txt
└── README.md
```

---

## 8. Segurança e Testes

* **Segurança:** Senhas com bcrypt, JWT para autenticação, isolamento de dados por usuário (user_id em todas queries)
* **Testes:** Pytest para validar regras de negócio e integração (6 testes passando)
* **Validação:** Pydantic v2 em todos endpoints

---

## 9. Deploy e Operação

* **Docker:** Multi-stage build, usuário não-root
* **Docker Compose:** PostgreSQL + API + Dashboard (+ ETL opcional)
* **Health Checks:** PostgreSQL (pg_isready), API (/health)
* **Makefile:** Comandos de desenvolvimento (install, test, run-api, docker-up, etc.)
* **Variáveis de ambiente:** .env para configuração