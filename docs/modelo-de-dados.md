# Modelo de Dados — 5 Centavos

## 1. Objetivo

Este documento apresenta o modelo de dados do **5 Centavos**: entidades, atributos, relacionamentos e regras de integridade que orientam a implementação do banco de dados.

O modelo foi projetado para o gerenciamento financeiro pessoal e para alimentar os processos de **Analytics, Engenharia de Dados e Inteligência Artificial** do projeto.

---

## 2. Visão geral

O banco de dados armazena informações relacionadas a:

* Usuários;
* Contas financeiras;
* Categorias;
* Transações;
* Metas financeiras.

As entidades são relacionadas de forma a garantir a integridade dos dados e o **isolamento das informações financeiras de cada usuário**.

### Relacionamento geral

```text
USUÁRIO
   │
   ├───────────────┬────────────┐
   ▼               ▼            ▼
 CONTAS        CATEGORIAS     METAS
   │               │
   └──────┬────────┘
          ▼
      TRANSAÇÕES
```

---

## 3. Entidades

### 3.1 Usuário — `users`

| Campo           | Tipo      | Restrições       | Descrição                          |
| --------------- | --------- | ---------------- | ---------------------------------- |
| `id`            | INTEGER   | PK               | Identificador único do usuário     |
| `name`          | VARCHAR   | NOT NULL         | Nome do usuário                    |
| `email`         | VARCHAR   | NOT NULL, UNIQUE, INDEX | E-mail do usuário           |
| `password_hash` | VARCHAR   | NOT NULL         | Senha em hash bcrypt               |
| `created_at`    | TIMESTAMP | NOT NULL         | Data de criação do cadastro        |

**Regras:** e-mail único; senha nunca em texto puro; usuário acessa apenas seus dados.

### 3.2 Conta financeira — `accounts`

| Campo             | Tipo      | Restrições              | Descrição             |
| ----------------- | --------- | ----------------------- | --------------------- |
| `id`              | INTEGER   | PK                      | Identificador da conta |
| `user_id`         | INTEGER   | FK → users, NOT NULL, `ON DELETE CASCADE` | Proprietário |
| `name`            | VARCHAR   | NOT NULL                | Nome da conta         |
| `type`            | ENUM      | NOT NULL                | `CORRENTE`, `POUPANCA`, `INVESTIMENTO`, `ESPECIE`, `CARTAO` |
| `initial_balance` | DECIMAL(14,2) | NOT NULL, DEFAULT 0 | Saldo inicial         |
| `created_at`      | TIMESTAMP | NOT NULL                | Data de criação       |

**Relacionamento:** `USUÁRIO 1 ─ N CONTAS`.

### 3.3 Categoria — `categories`

| Campo     | Tipo    | Restrições           | Descrição                  |
| --------- | ------- | -------------------- | -------------------------- |
| `id`      | INTEGER | PK                   | Identificador da categoria |
| `user_id` | INTEGER | FK → users, NOT NULL | Usuário proprietário       |
| `name`    | VARCHAR | NOT NULL             | Nome da categoria          |
| `type`    | ENUM    | NOT NULL             | `RECEITA` ou `DESPESA`     |

**Restrição adicional:** `UNIQUE (user_id, name, type)`.

**Relacionamento:** `USUÁRIO 1 ─ N CATEGORIAS`.

### 3.4 Transação — `transactions`

| Campo         | Tipo      | Restrições                         | Descrição                |
| ------------- | --------- | ---------------------------------- | ------------------------ |
| `id`          | INTEGER   | PK                                 | Identificador            |
| `account_id`  | INTEGER   | FK → accounts, NOT NULL, CASCADE   | Conta associada          |
| `category_id` | INTEGER   | FK → categories, NOT NULL, RESTRICT| Categoria associada      |
| `description` | VARCHAR   | NOT NULL                           | Descrição da movimentação|
| `amount`      | DECIMAL(14,2) | NOT NULL, CHECK `> 0`          | Valor da transação       |
| `type`        | ENUM      | NOT NULL                           | `RECEITA` ou `DESPESA`   |
| `date`        | DATE      | NOT NULL, INDEX                    | Data da movimentação     |
| `created_at`  | TIMESTAMP | NOT NULL                           | Data de registro         |

**Relacionamentos:** `CONTA 1 ─ N TRANSAÇÕES` e `CATEGORIA 1 ─ N TRANSAÇÕES`.

### 3.5 Meta financeira — `goals`

| Campo            | Tipo      | Restrições               | Descrição            |
| ---------------- | --------- | ------------------------ | -------------------- |
| `id`             | INTEGER   | PK                       | Identificador da meta|
| `user_id`        | INTEGER   | FK → users, NOT NULL     | Usuário proprietário |
| `name`           | VARCHAR   | NOT NULL                 | Nome da meta         |
| `target_amount`  | DECIMAL(14,2) | NOT NULL, CHECK `> 0` | Valor-alvo           |
| `current_amount` | DECIMAL(14,2) | NOT NULL, CHECK `>= 0` | Valor acumulado      |
| `deadline`       | DATE      | NULL                     | Data limite          |
| `created_at`     | TIMESTAMP | NOT NULL                 | Data de criação      |

**Relacionamento:** `USUÁRIO 1 ─ N METAS`.

---

## 4. Relacionamentos

| Origem    | Relação | Destino     |
| --------- | ------- | ----------- |
| Usuário   | 1:N     | Contas      |
| Usuário   | 1:N     | Categorias  |
| Usuário   | 1:N     | Metas       |
| Conta     | 1:N     | Transações  |
| Categoria | 1:N     | Transações  |

Ver [DER.md](DER.md) para o diagrama.

---

## 5. Chaves

**Primárias:** `id` em todas as tabelas.

**Estrangeiras:**

| Tabela         | Campo         | Referência      | Comportamento     |
| -------------- | ------------- | --------------- | ----------------- |
| `accounts`     | `user_id`     | `users.id`      | CASCADE           |
| `categories`   | `user_id`     | `users.id`      | CASCADE           |
| `transactions` | `account_id`  | `accounts.id`   | CASCADE           |
| `transactions` | `category_id` | `categories.id` | RESTRICT          |
| `goals`        | `user_id`     | `users.id`      | CASCADE           |

---

## 6. Integridade dos dados (DB)

* Conta/categoria/meta devem pertencer a um usuário existente;
* Transação deve estar vinculada a conta e categoria existentes;
* `amount > 0` e `target_amount > 0` garantidos por `CHECK CONSTRAINT`;
* Tipo (`RECEITA`/`DESPESA`, tipos de conta) garantido por `ENUM`;
* Unicidade de categoria por usuário+nome+tipo;
* Isolamento entre usuários aplicado na camada de serviços/repositórios.

## 7. Cálculo do saldo

```text
Saldo = Saldo Inicial + Receitas − Despesas
```

Derivado sob consulta (`AnalyticsRepository.account_transaction_totals`) — nunca persistido, evitando inconsistência em edições/exclusões.

## 8. Valores monetários

Valores financeiros utilizam `NUMERIC(14,2)` no banco e `Decimal` em Pydantic/`Decimal` em Python — nunca ponto flutuante.

## 9. Normalização

Estrutura em **3ª Forma Normal**: não há redundância (ex.: nomes de categoria não se repetem em transações — apenas `category_id`; o vínculo usuário↔transação ocorre via `account_id → accounts.user_id`).

## 10. Evolução futura

Possíveis entidades futuras (sem implementação atual, conforme necessidade):

* `budgets` — orçamentos financeiros;
* `recurring_transactions` — transações recorrentes;
* `attachments` — anexos de comprovantes;
* `notifications`, `audit_logs`, `imports`, `ai_insights`.

## 11. Tecnologias

| Versão  | Tecnologia                          |
| ------- | ----------------------------------- |
| V0.3.0  | SQLite                              |
| V0.4.0  | PostgreSQL                          |
| V0.4.0+ | SQLAlchemy                          |
| V0.5.0+ | API com FastAPI                     |
| V0.6.0+ | Pandas e Analytics                  |
| V1.1.0+ | SQLAlchemy 2.0 ORM declarativo      |
