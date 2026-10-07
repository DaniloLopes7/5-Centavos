# 5 Centavos

Plataforma de gerenciamento financeiro pessoal com foco em **Ciência de Dados, Analytics e Inteligência Artificial**.

## Sobre o projeto

O **5 Centavos** é uma ferramenta para organizar finanças pessoais, registrar receitas e despesas, acompanhar saldos e transformar esses dados em informações para tomada de decisão.

O objetivo é aplicar conceitos de **Programação, Banco de Dados, Engenharia de Dados, Analytics e IA** de forma prática.

## Objetivos

* Organizar receitas e despesas;
* Gerenciar contas financeiras;
* Acompanhar saldos;
* Categorizar transações;
* Gerar relatórios e indicadores;
* Analisar dados financeiros;
* Criar visualizações;
* Desenvolver processos de ETL;
* Aplicar Inteligência Artificial;
* Construir uma aplicação organizada e testável.

## Tecnologias

As tecnologias são adicionadas conforme a evolução do projeto.

| Tecnologia   | Utilização                     |
| ------------ | ------------------------------ |
| Python       | Linguagem principal            |
| PostgreSQL   | Banco de dados principal       |
| SQLAlchemy   | ORM                            |
| FastAPI      | Desenvolvimento da API REST    |
| Pandas       | Manipulação e análise de dados |
| NumPy        | Computação numérica            |
| Plotly       | Visualização de dados          |
| Streamlit    | Dashboard interativo           |
| Scikit-learn | Machine Learning               |
| Pytest       | Testes automatizados           |
| Docker       | Containerização                |
| python-jose  | Autenticação JWT               |

## Evolução do projeto

Desenvolvimento através de versões incrementais.

| Versão | Etapa                       | Status       |
| ------ | --------------------------- | ------------ |
| v0.1.0 | Planejamento e documentação | ✅ Finalizado |
| v0.2.0 | Estrutura inicial em Python | ✅ Finalizado |
| v0.3.0 | Sistema financeiro + SQLite | ✅ Finalizado |
| v0.4.0 | PostgreSQL + arquitetura    | ✅ Finalizado |
| v0.5.0 | API com FastAPI             | ✅ Finalizado |
| v0.6.0 | Analytics                   | ✅ Finalizado |
| v0.7.0 | Dashboard (Streamlit)       | ✅ Finalizado |
| v0.8.0 | Inteligência Artificial     | ✅ Finalizado |
| v1.0.0 | Docker + Deploy             | ✅ Finalizado |

> Cada versão é um marco funcional registrado via Git.

## Estrutura do projeto

```text
5-Centavos/
│
├── docs/
│   ├── especificacao.md
│   ├── requisitos.md
│   ├── regras-de-negocio.md
│   ├── casos-de-uso.md
│   ├── arquitetura.md
│   ├── modelo-de-dados.md
│   ├── DER.md
│   └── roadmap.md
│
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
│
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── requirements.txt
├── .dockerignore
├── .env.example
├── README.md
└── LICENSE
```

## Funcionalidades

### 🔐 Autenticação
- Registro de usuários com hash de senha (bcrypt)
- Login com JWT (JSON Web Tokens)
- Proteção de rotas com dependências FastAPI

### 🏦 Gestão Financeira
- **Contas**: Múltiplas contas por usuário (Corrente, Poupança, Investimento, Espécie, Cartão)
- **Transações**: Receitas e despesas com descrição, valor, data, categoria
- **Categorias**: Personalizáveis por usuário (Receita/Despesa)
- **Metas**: Objetivos financeiros com acompanhamento de progresso

### 📊 Analytics & Visualização
- Resumo financeiro (receitas, despesas, saldo, taxa de poupança)
- Gastos por categoria (gráficos de pizza e barras)
- Evolução mensal (receitas vs despesas vs saldo)
- Taxa de poupança automática

### 🤖 Inteligência Artificial
- **Classificador de transações**: Prediz categoria baseada na descrição
- **Detecção de anomalias**: Identifica gastos incomuns (Isolation Forest)
- **Previsão de fluxo de caixa**: Projeção de receitas/despesas futuras
- **Insights personalizados**: Sugestões baseadas em padrões de gasto
- **Perfil de gasto**: Clustering de comportamento financeiro

### 🐳 Docker & Deploy
- Multi-stage Dockerfile otimizado
- docker-compose com PostgreSQL, API, Dashboard
- Makefile para comandos de desenvolvimento
- Health checks e restart policies

## Conceitos aplicados

* Python & POO
* SQL e Bancos de Dados (PostgreSQL)
* APIs REST (FastAPI)
* Arquitetura de software (Clean Architecture)
* Engenharia de Dados e ETL
* Análise Exploratória de Dados
* Estatística e Visualização (Plotly/Streamlit)
* Machine Learning (Scikit-learn)
* Testes automatizados (Pytest)
* Git, Docker e CI/CD

## Como executar

### Pré-requisitos
- Python 3.11+
- PostgreSQL 16+
- Docker & Docker Compose (opcional)

### Opção 1: Docker (Recomendado)

```bash
# Clonar repositório
git clone <repo-url>
cd 5-Centavos

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas configurações

# Iniciar todos os serviços
docker-compose up -d

# Acessar:
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
# Dashboard: http://localhost:8501
```

### Opção 2: Desenvolvimento Local

```bash
# Criar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar banco PostgreSQL
# Criar database 'five_centavos' e usuário 'user'

# Configurar .env
cp .env.example .env
# Editar DATABASE_URL

# Executar ETL (cria tabelas e carrega dados)
python src/etl/load_data.py

# Iniciar API
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload

# Em outro terminal, iniciar Dashboard
streamlit run src/dashboard/app.py --server.port 8501
```

### Usando Makefile

```bash
make install      # Cria venv e instala dependências
make test         # Executa testes
make run-api      # Inicia API
make run-dashboard # Inicia Dashboard
make run-etl      # Executa ETL
make docker-up    # Inicia containers
make docker-down  # Para containers
```

## Endpoints da API

### Autenticação
- `POST /api/v1/auth/register` - Registrar usuário
- `POST /api/v1/auth/login` - Login (retorna JWT)
- `GET /api/v1/auth/me` - Usuário atual

### Contas
- `GET /api/v1/users/me/accounts` - Listar contas
- `POST /api/v1/users/me/accounts` - Criar conta
- `GET /api/v1/users/me/accounts/{id}` - Obter conta
- `PUT /api/v1/users/me/accounts/{id}` - Atualizar conta
- `DELETE /api/v1/users/me/accounts/{id}` - Remover conta

### Categorias
- `GET /api/v1/users/me/categories` - Listar categorias
- `POST /api/v1/users/me/categories` - Criar categoria
- `PUT /api/v1/users/me/categories/{id}` - Atualizar
- `DELETE /api/v1/users/me/categories/{id}` - Remover

### Transações
- `GET /api/v1/transactions` - Listar transações
- `POST /api/v1/transactions` - Criar transação
- `GET /api/v1/transactions/{id}` - Obter transação
- `PUT /api/v1/transactions/{id}` - Atualizar
- `DELETE /api/v1/transactions/{id}` - Remover

### Metas
- `GET /api/v1/goals` - Listar metas
- `POST /api/v1/goals` - Criar meta
- `POST /api/v1/goals/{id}/progress` - Adicionar progresso

### Analytics
- `GET /api/v1/analytics/summary` - Resumo financeiro
- `GET /api/v1/analytics/categories` - Por categoria
- `GET /api/v1/analytics/monthly` - Mensal

### Inteligência Artificial
- `POST /api/v1/ai/train` - Treinar modelos
- `POST /api/v1/ai/predict-category` - Predizer categoria
- `GET /api/v1/ai/insights` - Insights + previsões + anomalias
- `GET /api/v1/ai/cashflow-prediction` - Previsão fluxo de caixa
- `GET /api/v1/ai/anomalies` - Transações anômalas

## Testes

```bash
# Executar todos os testes
make test

# Ou diretamente
pytest tests/ -v
```

## Documentação

- [Especificação](docs/especificacao.md)
- [Requisitos](docs/requisitos.md)
- [Arquitetura](docs/arquitetura.md)
- [Modelo de Dados](docs/modelo-de-dados.md)
- [DER](docs/DER.md)
- [Regras de Negócio](docs/regras-de-negocio.md)
- [Casos de Uso](docs/casos-de-uso.md)
- [Roadmap](docs/roadmap.md)

## Autor

**Danilo Almeida Lopes**

Estudante de **Ciência de Dados**, interessado em Analytics, Engenharia de Dados e IA.

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.