# Changelog

Todas as mudanças notáveis deste projeto são documentadas neste arquivo.

O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/)
e o projeto adota [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [1.1.0] - 2026-10-12 — Reescrita profissional completa

Reescrita do zero de todo o código-fonte sobre a mesma especificação,
elevando o padrão de arquitetura, testes e observabilidade.

### Added
- Pacote Python único `cinco_centavos` (src layout) com `pyproject.toml`.
- Camada `core/` centralizando configuração (pydantic-settings), banco,
  segurança (bcrypt + JWT) e logging estruturado (structlog, JSON em produção).
- Exceções de domínio (`NotFoundError`, `ConflictError`, `BusinessRuleError`,
  `UnauthorizedError`) mapeadas centralmente para HTTP.
- Rate limiting (slowapi) nos endpoints de autenticação.
- ETL idempotente com relatório de registros criados x descartados e
  validação de compatibilidade categoria↔transação.
- Dashboard Streamlit reorganizado em páginas (visão geral, contas, transações,
  categorias, metas, IA), com cliente HTTP dedicado e componentes reutilizáveis.
- Entrypoint por modo (`api` | `dashboard` | `etl`) com espera do PostgreSQL.
- Health checks em todos os serviços do compose; perfil opcional `etl`.
- Dev local usa **SQLite por padrão** (`data/five_centavos.db`) — zero dependência
  de servidor; PostgreSQL do compose exposto no host pela porta **5433**
  (evita conflito com PostgreSQL local na 5432).

### Changed
- SQLAlchemy Core (queries textuais) → **ORM declarativo 2.0** com
  `Mapped`/`mapped_column`, relacionamentos, `CHECK`, `UNIQUE` e FKs com
  `CASCADE`/`RESTRICT`.
- Saldo de contas passa a ser derivado sob consulta (nunca persistido).
- Senhas com **bcrypt direto** (removido passlib).
- Suíte de testes: 6 → **41 testes** (unit, integration, e2e) com SQLite
  em memória isolado por teste; sem dependências externas.
- Docs atualizadas para refletir a nova arquitetura
  (arquitetura.md, requisitos.md, regras-de-negocio.md, casos-de-uso.md,
  modelo-de-dados.md, DER.md, roadmap.md).

### Removed
- Código legado das versões anteriores (CLI, módulos `cinco_centavos`
  antigos, ETL anterior e dashboard monolítico).
- `.env` rastreado no Git (agora apenas `.env.example`).

## [1.0.0] - 2024-10-07

### Added
- Dockerfile multi-stage com usuário não-root.
- docker-compose com PostgreSQL, API e Dashboard.
- Makefile com comandos de desenvolvimento.
- Health checks e restart policies.

## [0.8.0] — Inteligência Artificial

### Added
- TransactionClassifier (RandomForest), AnomalyDetector (IsolationForest),
  CashFlowPredictor (médias móveis), SpendingClusterer (K-Means) e
  FinancialAdvisor (orquestrador).
- Endpoints `/api/v1/ai/*`.

## [0.7.0] — Dashboard

### Added
- Dashboard Streamlit com gráficos Plotly.

## [0.6.0] — Analytics

### Added
- Resumo financeiro, por categoria e evolução mensal.

## [0.5.0] — API

### Added
- API REST com FastAPI e autenticação JWT.

## [0.4.0] — PostgreSQL + Arquitetura

### Changed
- Migração de SQLite para PostgreSQL com camadas Services/Repositories.

## [0.3.0] — Sistema financeiro

### Added
- Sistema financeiro funcional com SQLite.

## [0.2.0] — Estrutura inicial

### Added
- Estrutura inicial do projeto em Python.

## [0.1.0] — Planejamento

### Added
- Documentação inicial do projeto.
