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
Usuário -> Interface/UI (Streamlit) -> API (FastAPI) -> Services -> Persistence (SQLAlchemy) -> DB (SQLite/Postgres)
```

Os dados do banco alimentam as camadas de **Analytics e IA**.

---

# 4. Camadas

### 4.1 Interface
Responsável pela interação com o usuário: exibição de saldos, cadastro de transações e visualização de relatórios/gráficos.

### 4.2 API
Disponibiliza os recursos do sistema via REST (FastAPI). Valida requisições e encaminha para a camada de serviços.

### 4.3 Camada de Serviços
Contém as regras de negócio: cálculos de saldo, validações de transações e gestão de metas.

### 4.4 Camada de Persistência
Comunicação com o banco de dados via SQLAlchemy.

### 4.5 Banco de Dados
Armazenamento persistente. Inicia com **SQLite** e evolui para **PostgreSQL**.

---

# 5. Analytics e IA

**Analytics:** Transforma dados brutos em indicadores (Receitas/Despesas mensais, gastos por categoria) usando Pandas e NumPy.

**IA:** Implementação posterior para classificação de transações, detecção de anomalias e sugestões personalizadas.

---

# 6. Fluxo de Dados

```text
Usuário -> Interface -> API -> Services -> Repository -> Database -> Analytics/IA -> Dashboard -> Usuário
```

---

# 7. Organização do Código (Alvo)

```text
5-Centavos/
├── docs/
├── src/
│   ├── api/
│   ├── models/
│   ├── services/
│   ├── repositories/
│   ├── analytics/
│   └── ai/
├── tests/
├── data/
├── main.py
└── requirements.txt
```

---

# 8. Segurança e Testes

* **Segurança:** Senhas com hash, autenticação de usuários e isolamento de dados.
* **Testes:** Uso de **Pytest** para validar regras de negócio e integração.
