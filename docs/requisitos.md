# Requisitos — 5 Centavos

## 1. Objetivo

Definição dos requisitos funcionais e não funcionais que orientam o desenvolvimento do projeto.

Módulo raiz do código: `src/cinco_centavos/`.

## 2. Requisitos Funcionais

### RF01 — Cadastro de usuário ✅
Permitir a criação de contas de usuário, com categorias padrão criadas automaticamente.
**Implementado em:** `services/users.py` (`UserService.register`), `POST /api/v1/auth/register`

### RF02 — Autenticação ✅
Permitir login de usuários cadastrados com emissão de JWT.
**Implementado em:** `UserService.authenticate`, `POST /api/v1/auth/login`, `core/security.py`

### RF03 — Gerenciamento de contas ✅
Cadastrar, consultar, editar e remover contas financeiras.
**Implementado em:** `AccountService`, `AccountRepository`, endpoints `/api/v1/users/me/accounts`

### RF04 — Cadastro de receitas ✅
Registrar receitas (valor, descrição, categoria, conta e data).
**Implementado em:** `TransactionService.create_transaction` com tipo `RECEITA`

### RF05 — Cadastro de despesas ✅
Registrar despesas (valor, descrição, categoria, conta e data).
**Implementado em:** `TransactionService.create_transaction` com tipo `DESPESA`

### RF06 — Gerenciamento de categorias ✅
Criar e gerenciar categorias financeiras (únicas por usuário + nome + tipo).
**Implementado em:** `CategoryService`, endpoints `/api/v1/users/me/categories`

### RF07 — Consulta de saldo ✅
Calcular e exibir o saldo das contas (inicial + receitas − despesas).
**Implementado em:** `AccountService` + `AnalyticsRepository.account_transaction_totals`

### RF08 — Consulta de transações ✅
Consultar o histórico com filtros por conta, tipo e período.
**Implementado em:** `TransactionService.list_transactions`, `GET /api/v1/transactions`

### RF09 — Edição e exclusão de transações ✅
Permitir a alteração ou remoção de transações com reflexo imediato no saldo.
**Implementado em:** `TransactionService.update_transaction/delete_transaction`

### RF10 — Relatórios financeiros ✅
Gerar relatórios de receitas, despesas e saldos por período.
**Implementado em:** `AnalyticsService.get_financial_summary`, `GET /api/v1/analytics/summary`

### RF11 — Indicadores financeiros ✅
Taxa de poupança, totais, contagens e destaques por categoria.
**Implementado em:** `AnalyticsService`, endpoints `/api/v1/analytics/*`

### RF12 — Análise de dados ✅
Agregações por categoria e por mês com percentuais e médias.
**Implementado em:** `AnalyticsService`, `AnalyticsRepository`

### RF13 — Visualização de dados ✅
Gráficos de pizza (categorias) e linhas (evolução mensal) no dashboard.
**Implementado em:** Dashboard Streamlit com Plotly (`dashboard/components.py`)

### RF14 — Importação de dados ✅
Importar transações e dados iniciais via arquivos CSV, descartando registros inválidos.
**Implementado em:** `cinco_centavos.etl.load_data` + `data/*.csv`

### RF15 — Exportação de dados ⏳
Exportar dados financeiros (CSV/Excel/PDF).
**Status:** Planejado para próxima iteração.

### RF16 — Metas financeiras ✅
Criar e acompanhar metas de economia com progresso incremental.
**Implementado em:** `GoalService`, endpoints `/api/v1/goals` e `POST /api/v1/goals/{id}/progress`

### RF17 — Inteligência Artificial ✅
Classificação de categorias, detecção de anomalias, previsão de fluxo de caixa, perfis de gasto e insights.
**Implementado em:** `cinco_centavos.ai` (5 modelos), endpoints `/api/v1/ai/*`

---

## 3. Requisitos Não Funcionais

### RNF01 — Segurança ✅
Bcrypt para senhas, JWT para autenticação, rate limiting em endpoints sensíveis (slowapi), container não-root.

### RNF02 — Privacidade ✅
Todas as queries filtram por `user_id`; acesso a recursos de terceiros responde 404.

### RNF03 — Desempenho ✅
Connection pooling, `pool_pre_ping`, índices em PK/FK e colunas de filtro, agregações no banco.

### RNF04 — Manutenibilidade ✅
Arquitetura em camadas: API → Services → Repositories → Models, com Schemas Pydantic na fronteira.

### RNF05 — Escalabilidade ✅
API stateless, PostgreSQL, containers separados por responsabilidade.

### RNF06 — Testabilidade ✅
Pytest com 41 testes: unitários (services, IA), integração (API) e e2e (jornadas).

### RNF07 — Portabilidade ✅
Python 3.11+, dependências pinadas em `requirements.txt`, Docker multi-stage.

### RNF08 — Documentação ✅
Docs em `docs/`, OpenAPI/Swagger automático em `/docs`, docstrings e README.

### RNF09 — Versionamento ✅
Git com commits semânticos, CHANGELOG.md e SemVer.

### RNF10 — Containerização ✅
Dockerfile multi-stage, docker-compose (db, api, dashboard, etl), health checks e restart policies.

---

## 4. Prioridades

### ✅ Concluídos (Alta)
Cadastro, Autenticação, Contas, Receitas, Despesas, Categorias, Saldo, Transações

### ✅ Concluídos (Média)
Relatórios, Indicadores, Metas, Importação (ETL), Analytics, Dashboard

### ✅ Concluídos (Baixa/Futura)
IA (Classificação, Anomalias, Previsão, Insights, Clustering), Docker + Deploy

### ⏳ Planejado
RF15 — Exportação de dados (CSV/Excel/PDF)

---

## 5. Evolução

Requisitos refinados ao longo das versões v0.1.0–v1.0.0. Em **v1.1.0** o código-fonte foi reescrito do zero sobre a mesma especificação, com arquitetura em camadas, ORM declarativo, observabilidade estruturada e suíte de testes ampliada.
