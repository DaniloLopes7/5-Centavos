# Roadmap — 5 Centavos

## 1. Objetivo

Este documento organiza a evolução do **5 Centavos** em etapas e versões, desde o planejamento até a entrega de uma solução completa com Analytics e IA.

---

# 2. Visão geral

Evolução planejada:
v0.1.0 (Planejamento) → v0.2.0 (Python) → v0.3.0 (SQLite) → v0.4.0 (Postgres) → v0.5.0 (API) → v0.6.0 (Analytics) → v0.7.0 (Dashboard) → v0.8.0 (IA) → v1.0.0 (Deploy)

---

# 3. Roadmap de versões

## v0.1.0 — Planejamento e documentação
**Objetivo:** Base conceitual e técnica.
* Documentação, requisitos, regras de negócio, modelo de dados e README.
**Status:** ✅ Finalizado

---

## v0.2.0 — Estrutura inicial em Python
**Objetivo:** Primeira estrutura executável.
* Configuração do ambiente, módulos iniciais e primeiros testes.
**Status:** ✅ Finalizado

---

## v0.3.0 — Sistema financeiro + SQLite
**Objetivo:** Primeira versão funcional do gerenciamento.
* Cadastro de usuários, contas, categorias, transações e cálculo de saldo.
* Persistência em SQLite.
**Status:** ✅ Finalizado

---

## v0.4.0 — PostgreSQL + arquitetura
**Objetivo:** Evoluir para arquitetura profissional.
* Migração para PostgreSQL e organização em camadas (Services/Repositories).
* SQLAlchemy Core e testes automatizados.
**Status:** ✅ Finalizado

---

## v0.5.0 — API REST (FastAPI)
**Objetivo:** Disponibilizar recursos via API REST.
* Endpoints com FastAPI, autenticação JWT, documentação OpenAPI/Swagger.
* Endpoints: Auth, Users, Accounts, Categories, Transactions, Goals.
**Status:** ✅ Finalizado

---

## v0.6.0 — Analytics
**Objetivo:** Gerar indicadores a partir dos dados.
* Analytics Service/Repository com resumos financeiros.
* Análise por categoria, evolução mensal, indicadores financeiros.
* Integração com API e Dashboard.
**Status:** ✅ Finalizado

---

## v0.7.0 — Dashboard (Streamlit)
**Objetivo:** Interface visual para os dados.
* Dashboard interativo com Streamlit e gráficos Plotly.
* Páginas: Dashboard, Contas, Transações, Categorias, Metas, Analytics.
* Integração completa com API via HTTP.
**Status:** ✅ Finalizado

---

## v0.8.0 — Inteligência Artificial
**Objetivo:** Análises e sugestões inteligentes.
* Classificação automática de transações (RandomForest).
* Detecção de anomalias/gastos incomuns (Isolation Forest).
* Previsão de fluxo de caixa (médias móveis).
* Insights personalizados e sugestões de economia.
* Clustering de perfis de gasto (K-Means).
* API endpoints para IA: /ai/train, /ai/insights, /ai/predict-category, /ai/anomalies.
**Status:** ✅ Finalizado

---

## v1.0.0 — Docker + Deploy
**Objetivo:** Preparar para produção.
* Dockerfile multi-stage otimizado.
* Docker Compose com PostgreSQL + API + Dashboard (+ ETL opcional).
* Makefile para comandos de desenvolvimento.
* Health checks, restart policies, usuário não-root.
* .dockerignore, .env.example, Makefile.
**Status:** ✅ Finalizado

---

# 4. Estratégia de versionamento

O projeto usa um único repositório. O histórico é mantido via commits e tags Git.

---

# 5. Status atual

**Versão atual:** v1.0.0
**Etapa:** ✅ Todas as versões planejadas concluídas
**Próximos passos sugeridos:**
- CI/CD com GitHub Actions
- Testes de integração da API
- Testes end-to-end do Dashboard
- Monitoramento (Prometheus/Grafana)
- Logs estruturados (structlog)
- Rate limiting na API
- Backup automatizado do PostgreSQL
- Internacionalização (i18n)

---

# 6. Entregas por versão

| Versão | Entregas Principais |
|--------|---------------------|
| v0.1.0 | Docs: especificação, requisitos, regras, casos de uso, modelo de dados, DER, arquitetura, roadmap |
| v0.2.0 | Estrutura src/, database.py inicial, main.py CLI, requirements.txt |
| v0.3.0 | CRUD completo (users, accounts, categories, transactions, goals), saldo, CLI funcional, SQLite, ETL básico |
| v0.4.0 | PostgreSQL, SQLAlchemy Core, Services/Repositories, Pytest (6 testes), arquitetura em camadas |
| v0.5.0 | FastAPI, JWT auth, Pydantic v2, endpoints completos, Swagger/OpenAPI, deps |
| v0.6.0 | AnalyticsService/Repository, resumos, categorias, mensal, integração API |
| v0.7.0 | Streamlit app, 6 páginas, Plotly charts, integração API, navegação sidebar |
| v0.8.0 | 5 modelos ML, FinancialAdvisor, endpoints IA, treino automático |
| v1.0.0 | Dockerfile, docker-compose.yml, Makefile, .dockerignore, healthchecks, volumes |