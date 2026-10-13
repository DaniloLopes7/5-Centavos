# Roadmap — 5 Centavos

## Linha de evolução

| Versão | Objetivo                          | Status       |
| ------ | --------------------------------- | ------------ |
| v0.1.0 | Planejamento e documentação       | ✅ Finalizado |
| v0.2.0 | Estrutura inicial em Python       | ✅ Finalizado |
| v0.3.0 | Sistema financeiro + SQLite/CLI   | ✅ Finalizado |
| v0.4.0 | PostgreSQL + arquitetura em camadas | ✅ Finalizado |
| v0.5.0 | API REST com FastAPI + JWT        | ✅ Finalizado |
| v0.6.0 | Analytics (resumos, indicadores)  | ✅ Finalizado |
| v0.7.0 | Dashboard Streamlit + Plotly      | ✅ Finalizado |
| v0.8.0 | Inteligência Artificial (5 modelos) | ✅ Finalizado |
| v1.0.0 | Docker multi-stage + Compose + Makefile | ✅ Finalizado |
| v1.1.0 | Reescrita profissional completa   | ✅ **Atual**  |

## v1.1.0 — Reescrita profissional (2026-10-12)

Recorte desta versão:

* Pacote Python único `cinco_centavos` (src layout) com `pyproject.toml`;
- SQLAlchemy 2.0 **ORM declarativo** (antes: Core com queries textuais);
- Camadas formais: API → Services → Repositories → Models (+ Schemas na fronteira);
- Exceções de domínio mapeadas para HTTP de forma centralizada;
- Logging estruturado (structlog) e rate limiting (slowapi) na autenticação;
- ETL idempotente com relatório de criados/descartados;
- Dashboard Streamlit reorganizado em páginas (visão geral, contas, transações, categorias, metas, IA);
- Suíte de testes ampliada para **41 testes** (unit/integration/e2e);
- Docker com usuário não-root, health checks em todos os serviços e entrypoint por modo (`api`/`dashboard`/`etl`).

## Próximos passos sugeridos

| Prioridade | Item                                                |
| ---------- | --------------------------------------------------- |
| Curto      | RF15 — Exportação de dados (CSV/Excel/PDF)          |
| Curto      | CI/CD (GitHub Actions): lint + testes + build Docker |
| Médio      | Migrações com Alembic                               |
| Médio      | Monitoramento (Prometheus/Grafana) e alertas         |
| Médio      | Transações recorrentes e orçamentos (`budgets`)      |
| Baixo      | Internacionalização (i18n)                           |
| Baixo      | Persistência de insights de IA (`ai_insights`)       |
