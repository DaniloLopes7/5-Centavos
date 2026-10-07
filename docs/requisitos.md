# Requisitos — 5 Centavos

## 1. Objetivo

Definição dos requisitos funcionais e não funcionais para orientar o desenvolvimento do projeto.

## 2. Requisitos Funcionais

### RF01 — Cadastro de usuário ✅
Permitir a criação de contas de usuário.
**Implementado em:** `UserService.register()`, `POST /api/v1/auth/register`

### RF02 — Autenticação ✅
Permitir login de usuários cadastrados.
**Implementado em:** `UserService.authenticate()`, `POST /api/v1/auth/login` (JWT)

### RF03 — Gerenciamento de contas ✅
Cadastrar, consultar, editar e remover contas financeiras.
**Implementado em:** `AccountService`, `AccountRepository`, endpoints `/users/me/accounts`

### RF04 — Cadastro de receitas ✅
Registrar receitas (valor, descrição, categoria, conta e data).
**Implementado em:** `TransactionService.create()` com tipo RECEITA, `POST /api/v1/transactions`

### RF05 — Cadastro de despesas ✅
Registrar despesas (valor, descrição, categoria, conta e data).
**Implementado em:** `TransactionService.create()` com tipo DESPESA, `POST /api/v1/transactions`

### RF06 — Gerenciamento de categorias ✅
Criar e gerenciar categorias financeiras.
**Implementado em:** `CategoryService`, `CategoryRepository`, endpoints `/users/me/categories`

### RF07 — Consulta de saldo ✅
Calcular e exibir o saldo das contas.
**Implementado em:** `AccountService.calculate_balance()`, `GET /users/me/accounts`

### RF08 — Consulta de transações ✅
Consultar o histórico de transações do usuário.
**Implementado em:** `TransactionService.get_user_transactions()`, `GET /api/v1/transactions`

### RF09 — Edição e exclusão de transações ✅
Permitir a alteração ou remoção de transações.
**Implementado em:** `TransactionService.update()/delete()`, `PUT/DELETE /api/v1/transactions/{id}`

### RF10 — Relatórios financeiros ✅
Gerar relatórios de receitas, despesas e saldos.
**Implementado em:** `AnalyticsService.get_financial_summary()`, `GET /api/v1/analytics/summary`

### RF11 — Indicadores financeiros ✅
Apresentar indicadores da situação financeira.
**Implementado em:** `AnalyticsService`, endpoints `/api/v1/analytics/*`, Dashboard

### RF12 — Análise de dados ✅
Realizar análises utilizando técnicas de Analytics.
**Implementado em:** `AnalyticsService`, `AnalyticsRepository`, `src/analytics/`

### RF13 — Visualização de dados ✅
Apresentar dados via gráficos e visualizações.
**Implementado em:** Dashboard Streamlit com Plotly (pizza, barras, linhas, scatter)

### RF14 — Importação de dados ✅
Importar transações via arquivos CSV.
**Implementado em:** ETL (`src/etl/load_data.py`) carrega CSVs iniciais

### RF15 — Exportação de dados ⏳
Exportar dados financeiros.
**Status:** Planejado para próxima iteração (CSV/Excel/PDF)

### RF16 — Metas financeiras ✅
Criar e acompanhar metas de economia.
**Implementado em:** `GoalService`, `GoalRepository`, endpoints `/api/v1/goals`, Dashboard

### RF17 — Inteligência Artificial ✅
Utilizar IA para análises e sugestões automáticas.
**Implementado em:** `src/ai/` (5 modelos), `FinancialAdvisor`, endpoints `/api/v1/ai/*`

---

## 3. Requisitos Não Funcionais

### RNF01 — Segurança ✅
Proteção de dados e armazenamento de senhas via hash (bcrypt).
**Implementado:** bcrypt para senhas, JWT para autenticação, isolamento por user_id

### RNF02 — Privacidade ✅
Acesso restrito aos próprios dados do usuário.
**Implementado:** Todas queries filtram por `user_id`, validação em Services

### RNF03 — Desempenho ✅
Eficiência em operações comuns.
**Implementado:** Connection pooling SQLAlchemy, queries otimizadas, índices PK/FK

### RNF04 — Manutenibilidade ✅
Código modular e organizado.
**Implementado:** Arquitetura em camadas (API, Services, Repositories, Schemas, AI)

### RNF05 — Escalabilidade ✅
Arquitetura que permita a evolução do sistema.
**Implementado:** Arquitetura em camadas, PostgreSQL, Docker, stateless API

### RNF06 — Testabilidade ✅
Implementação de testes automatizados nas funções principais.
**Implementado:** Pytest (6 testes passando), cobertura Services/Repositories

### RNF07 — Portabilidade ✅
Execução em ambientes compatíveis com as dependências.
**Implementado:** Docker multi-stage, Python 3.11+, requirements.txt

### RNF08 — Documentação ✅
Documentar funcionalidades e decisões técnicas.
**Implementado:** Docs completas, Swagger/OpenAPI, README, docstrings

### RNF09 — Versionamento ✅
Uso de Git para histórico de alterações.
**Implementado:** Git repo com tags por versão, commits semânticos

### RNF10 — Containerização ✅
Execução via containers Docker.
**Implementado:** Dockerfile multi-stage, docker-compose.yml, Makefile

---

## 4. Prioridades (Atualizado)

### ✅ Concluídos (Alta)
* Cadastro, Autenticação, Contas, Receitas, Despesas, Categorias, Saldo, Transações, Metas

### ✅ Concluídos (Média)
* Relatórios, Indicadores, Metas, Importação (ETL), Analytics, Dashboard

### ✅ Concluídos (Baixa/Futura - Agora Concluídos)
* IA (Classificação, Anomalias, Previsão, Insights, Clustering)
* Docker (Multi-stage, Compose, Makefile), Deploy

---

## 5. Evolução
Os requisitos foram refinados e **todos implementados** conforme as versões v0.1.0 a v1.0.0.