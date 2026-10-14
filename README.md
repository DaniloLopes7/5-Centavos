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
| Python 3.12+   | Linguagem principal                 |
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
- **A landing page é a porta de entrada única** (`landing/`): cadastro ou login nela fazem auto-login e redirecionam ao dashboard definido por `window.DASHBOARD_URL` em `landing/config.js`, levando o token JWT
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
- Docker & Docker Compose **ou** Python 3.12+ (dev local usa SQLite, sem servidor de banco)

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

## Deploy

Em produção, cada parte roda no serviço adequado: landing estática na Vercel, API FastAPI em um serviço Python com PostgreSQL, e dashboard Streamlit no Streamlit Community Cloud ou em outro serviço persistente. A Vercel não inicia a API Python nem o Streamlit.

### 1. Landing estática na Vercel

1. Mantenha o **Root Directory** do projeto como `.` (raiz do repositório). O `vercel.json` seleciona o preset `Other` e publica somente `landing/` como diretório de saída; não configure um comando de build.
2. Depois de criar a API e o dashboard, substitua os dois valores de exemplo em `landing/config.js` por suas URLs públicas (`window.API_URL` e `window.DASHBOARD_URL`). Essa configuração é JavaScript estático e não recebe variáveis de ambiente da Vercel durante a execução no navegador.
3. Faça push para a branch conectada à Vercel. O HTML, CSS, JavaScript e imagens presentes em `landing/` serão publicados como arquivos estáticos.

### 2. API e PostgreSQL no Render

1. No Render, crie um **Blueprint** conectado a este repositório. O `render.yaml` prepara um serviço Python em modo API e um PostgreSQL gerenciado na mesma região. Os planos definidos são pagos; revise ou ajuste os planos no YAML antes de sincronizar o Blueprint.
2. O Blueprint injeta `DATABASE_URL`, gera `SECRET_KEY` e define `APP_ENV=production`. A API normaliza a URL do PostgreSQL para `postgresql+psycopg2://...`; se usar um banco externo que exija TLS, acrescente `?sslmode=require` à URL.
3. Quando o deploy terminar, valide `https://<api>.onrender.com/health`; a resposta esperada contém `"status":"ok"`. O caminho `/docs` abre a documentação REST.
4. O CORS já inclui `https://5-centavos.vercel.app`. Se mudar o domínio da landing, atualize `CORS_ORIGINS` nas variáveis do serviço.

O segredo de produção precisa ter pelo menos 32 caracteres. A API para a inicialização com uma mensagem clara se `SECRET_KEY` estiver ausente ou tiver o valor de exemplo. Não reutilize o valor local de `.env.example` em produção.

### 3. Dashboard Streamlit fora da Vercel

No Streamlit Community Cloud, crie um app apontando para `src/cinco_centavos/dashboard/app.py`, selecione Python 3.12 e, em **Advanced settings → Secrets**, configure:

```toml
API_URL = "https://<api>.onrender.com"
LANDING_URL = "https://5-centavos.vercel.app"
```

O dashboard lê `API_URL` e `LANDING_URL` das variáveis de ambiente e, no Community Cloud, também de `st.secrets`. Para rodá-lo em um host com Docker, use o modo `dashboard` do `entrypoint.sh` e passe `API_URL` apontando para a API (por exemplo, `http://api:8000` dentro do Compose) e `LANDING_URL` apontando para a landing pública. O Streamlit precisa de um serviço com processo persistente e suporte a WebSocket.

### Variáveis de ambiente

`.env.example` lista as variáveis locais e documenta as URLs públicas que devem ser copiadas para `landing/config.js`. No Render, `DATABASE_URL` e `SECRET_KEY` são configuradas pelo Blueprint; no serviço do dashboard configure `API_URL` e `LANDING_URL`. Não versione `.env` nem `secrets.toml`.

O Aurora DSQL conectado pelo Marketplace da Vercel não é usado por esta arquitetura separada: a API passa a rodar no Render e usa o PostgreSQL associado ao Blueprint. Para usar DSQL nesse desenho, seria necessário configurar autenticação AWS disponível diretamente ao serviço da API.

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
