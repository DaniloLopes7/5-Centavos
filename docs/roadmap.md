# Roadmap — 5 Centavos

## 1. Objetivo

Este documento organiza a evolução do **5 Centavos** em etapas e versões, desde o planejamento até a entrega de uma solução completa com Analytics e IA.

---

# 2. Visão geral

Evolução planejada:
v0.1.0 (Planejamento) -> v0.2.0 (Python) -> v0.3.0 (SQLite) -> v0.4.0 (Postgres) -> v0.5.0 (API) -> v0.6.0 (Analytics) -> v0.7.0 (Dashboard) -> v0.8.0 (IA) -> v1.0.0 (Deploy)

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
* SQLAlchemy e testes automatizados.
**Status:** 🔄 Em desenvolvimento

---

## v0.5.0 — API
**Objetivo:** Disponibilizar recursos via API REST.
* Endpoints com FastAPI, autenticação e documentação da API.
**Status:** ⏳ Pendente

---

## v0.6.0 — Analytics
**Objetivo:** Gerar indicadores a partir dos dados.
* Processos de ETL, análise exploratória e indicadores financeiros.
**Status:** ⏳ Pendente

---

## v0.7.0 — Dashboard
**Objetivo:** Interface visual para os dados.
* Dashboard com Streamlit e gráficos com Plotly.
**Status:** ⏳ Pendente

---

## v0.8.0 — Inteligência Artificial
**Objetivo:** Análises e sugestões inteligentes.
* Classificação de transações, detecção de anomalias e previsões.
**Status:** ⏳ Pendente

---

## v1.0.0 — Docker + Deploy
**Objetivo:** Preparar para produção.
* Dockerfile, Docker Compose e deploy da aplicação.
**Status:** ⏳ Pendente

---

# 4. Estratégia de versionamento

O projeto usa um único repositório. O histórico é mantido via commits e tags Git.

# 5. Status atual

**Versão atual:** v0.3.0
**Etapa:** Sistema financeiro + SQLite
**Próxima versão:** v0.4.0 — PostgreSQL + arquitetura
**Situação:** ✅ Finalizado
