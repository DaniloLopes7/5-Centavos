# 5 Centavos 🪙

Plataforma de gestão financeira pessoal com foco em **Ciência de Dados, Analytics e Inteligência Artificial**.

## Sobre o projeto

O **5 Centavos** organiza finanças pessoais: registre receitas e despesas, gerencie contas e metas, e transforme os dados em indicadores, previsões e insights acionáveis gerados por IA.

Arquitetura em camadas, testável e pronta para deploy via Docker:

```text
Landing page (HTML/CSS/JS) → Dashboard (Streamlit) → API REST (FastAPI) → Services → Repositories → PostgreSQL
                                                                  ↘ Analytics & IA (Scikit-learn)
```

## Tecnologias

| Tecnologia     | Utilização                          |
| -------------- | ----------------------------------- |
| Python 3.11+   | Linguagem principal                 |
| PostgreSQL 16  | Banco de dados principal            |
| SQLAlchemy 2.0 | ORM (modelos declarativos)          |
| FastAPI        | API REST + OpenAPI/Swagger          |
| Pydantic v2    | Validação de contratos              |
| python-jose + bcrypt | JWT e hash de senhas           |
| Scikit-learn   | Machine Learning (5 modelos)        |
| Pandas/NumPy   | Manipulação e análise de dados      |
| Streamlit      | Dashboard interativo                |
| Plotly         | Visualizações                       |
| structlog      | Logging estruturado                 |
| slowapi        | Rate limiting                       |
| Pytest/httpx   | Testes automatizados                |
| Docker         | Containerização                     |

## Funcionalidades

### 🔐 Autenticação
- **A landing page é a porta de entrada única** (`landing/`): cadastro ou login nela fazem auto-login e redirecionam ao dashboard em `:8501` com o token JWT
- Registro com hash bcrypt e categorias padrão automáticas
- Login com JWT; isolamento total de dados por usuário

### 🎨 Design System ("Clareza que vale ouro")
- Landing de conversão (12 seções) e dashboard Streamlit compartilham a mesma identidade: branco/off-white + amarelo #FFC72C + grafite, Plus Jakarta Sans/Inter, bordas grandes e sombras quentes
- Tema do Streamlit: `.streamlit/config.toml` + CSS injetado por `dashboard/theme.py` — aplicado a todas as páginas do painel

### 🏦 Gestão Financeira
- **Contas**: CRUD completo com saldo calculado (inicial + receitas − despesas)
- **Transações**: receitas/despesas com validações de valor, data e tipo
- **Categorias**: personalizáveis por usuário; unicidade nome+tipo
- **Metas**: objetivos financeiros com progresso incremental

### 📊 Analytics & Visualização
- Resumo financeiro com taxa de poupança
- Totais por categoria (com percentuais) e evolução mensal
- Dashboard Streamlit com gráficos Plotly (pizza e linhas)

### 🤖 Inteligência Artificial
- **Classificador de transações**: TF-IDF + RandomForest
- **Detecção de anomalias**: Isolation Forest
- **Previsão de fluxo de caixa**: médias móveis
- **Perfil de consumo**: K-Means
- **Insights transparentes**: FinancialAdvisor explica os fatores de cada análise
- Mínimo de 8 transações do usuário para treinar os modelos

### 🐳 Docker & Deploy
- Multi-stage build, usuário não-root, health checks
- docker-compose: PostgreSQL + API + Dashboard (+ ETL opcional)
- Makefile, `.env` e entrypoint por modo (`api`/`dashboard`/`etl`)

## Como executar

### Pré-requisitos
- Docker & Docker Compose **ou** Python 3.11+ (dev local usa SQLite, sem servidor de banco)

### Opção 1 — Docker (recomendado)

```bash
cp .env.example .env   # ajuste SECRET_KEY e credenciais

docker compose up -d --build

# ETL de dados de exemplo (opcional)
docker compose --profile etl run --rm etl
# ou configure RUN_ETL=true no .env antes de subir

# Acessos:
#   Landing:   http://localhost:8080   →  python3 -m http.server 8080 --directory landing
#   API/REST:  http://localhost:8000/docs
#   Dashboard: http://localhost:8501   (entrar/cadastrar pela landing — ela redireciona)
```

### Opção 2 — Local

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# Opcional: cp .env.example .env (o padrão já é SQLite em data/five_centavos.db)

PYTHONPATH=src python -m cinco_centavos.etl.load_data        # seed inicial (opcional)
PYTHONPATH=src uvicorn cinco_centavos.api.main:app --reload  # API em :8000
PYTHONPATH=src streamlit run src/cinco_centavos/dashboard/app.py  # Dashboard :8501
```

> Para usar PostgreSQL no dev local, suba apenas o banco com
> `docker compose up -d db` (exposto na porta **5433** do host) e configure
> `DATABASE_URL=postgresql+psycopg2://user:password@localhost:5433/five_centavos`.

### Makefile

```bash
make install        # venv + dependências
make run-etl        # carga dos CSVs em data/
make run-api        # API com reload
make run-dashboard  # Streamlit
make test           # suíte completa (unit + integration + e2e)
make docker-up      # containers
```

## Endpoints da API

### Autenticação
- `POST /api/v1/auth/register` — registrar usuário
- `POST /api/v1/auth/login` — login (JWT)
- `GET /api/v1/auth/me` — usuário autenticado

### Contas (`/api/v1/users/me/accounts`)
- `GET` listar com saldo · `POST` criar · `GET/PUT/DELETE /{id}`

### Categorias (`/api/v1/users/me/categories`)
- `GET` listar (filtro `type`) · `POST` criar · `PUT/DELETE /{id}`

### Transações (`/api/v1/transactions`)
- `GET` listar (filtros `account_id`, `type`, `start_date`, `end_date`)
- `POST` criar · `GET/PUT/DELETE /{id}`

### Metas (`/api/v1/goals`)
- `GET` listar · `POST` criar · `GET/PUT/DELETE /{id}` · `POST /{id}/progress`

### Analytics (`/api/v1/analytics`)
- `GET /summary` — resumo consolidado
- `GET /categories` — totais por categoria
- `GET /monthly` — evolução mensal

### IA (`/api/v1/ai`)
- `POST /train` — treina os modelos com seus dados
- `POST /predict-category` — prediz categoria de uma descrição
- `GET /insights` — insights + perfil + previsão
- `GET /cashflow-prediction` — previsão de fluxo de caixa
- `GET /anomalies` — gastos fora do padrão

### Infra
- `GET /health` — health check

## Testes

```bash
make test                 # 41 testes: unit, integration, e2e
make test-unit            # apenas serviços/IA
make test-integration     # API e jornadas e2e
```

Os testes usam SQLite em memória isolado por teste — nenhum serviço externo é necessário.

## Estrutura

```text
5-Centavos/
├── landing/           # Landing page + cadastro/login (HTML, CSS, JS puros — porta de entrada)
├── .streamlit/        # Tema do dashboard (config.toml)
├── src/cinco_centavos/
│   ├── core/          # config, database (SQLAlchemy), security (bcrypt+JWT), logging
│   ├── models/        # ORM: User, Account, Category, Transaction, Goal + enums
│   ├── schemas/       # contratos Pydantic v2 por domínio
│   ├── repositories/  # acesso a dados com isolamento por usuário
│   ├── services/      # regras de negócio + exceções de domínio
│   ├── api/           # FastAPI: main, rate limit, v1 (deps/router/endpoints por domínio)
│   ├── ai/            # 5 modelos de IA + FinancialAdvisor
│   ├── etl/           # importação CSV idempotente com validação
│   └── dashboard/     # Streamlit: app, theme (design system), api_client, components, views/
├── tests/             # unit / integration / e2e
├── data/              # CSVs seed
├── docs/              # especificação, requisitos, RN, CU, arquitetura, modelo, DER, roadmap
├── Dockerfile / docker-compose.yml / Makefile / entrypoint.sh
└── pyproject.toml / requirements.txt
```

## Documentação

- [Especificação](docs/especificacao.md)
- [Requisitos](docs/requisitos.md)
- [Regras de Negócio](docs/regras-de-negocio.md)
- [Casos de Uso](docs/casos-de-uso.md)
- [Arquitetura](docs/arquitetura.md)
- [Modelo de Dados](docs/modelo-de-dados.md) · [DER](docs/DER.md)
- [Roadmap](docs/roadmap.md) · [CHANGELOG](CHANGELOG.md)

## Autor

**Danilo Almeida Lopes** — estudante de Ciência de Dados.

## Licença

MIT — veja [LICENSE](LICENSE).
