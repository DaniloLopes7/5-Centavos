# DER — Diagrama Entidade-Relacionamento (5 Centavos)

## Entidades e relacionamentos

```mermaid
erDiagram
    USER ||--o{ ACCOUNT : possui
    USER ||--o{ CATEGORY : possui
    USER ||--o{ GOAL : possui
    ACCOUNT ||--o{ TRANSACTION : registra
    CATEGORY ||--o{ TRANSACTION : classifica

    USER {
        int id PK
        varchar name
        varchar email UK
        varchar password_hash
        datetime created_at
    }

    ACCOUNT {
        int id PK
        int user_id FK
        varchar name
        varchar type "CORRENTE|POUPANCA|INVESTIMENTO|ESPECIE|CARTAO"
        decimal initial_balance
        datetime created_at
    }

    CATEGORY {
        int id PK
        int user_id FK
        varchar name
        varchar type "RECEITA|DESPESA"
    }

    TRANSACTION {
        int id PK
        int account_id FK
        int category_id FK
        varchar description
        decimal amount "CHECK (amount > 0)"
        varchar type "RECEITA|DESPESA"
        date date
        datetime created_at
    }

    GOAL {
        int id PK
        int user_id FK
        varchar name
        decimal target_amount "CHECK (target_amount > 0)"
        decimal current_amount "CHECK (current_amount >= 0)"
        date deadline
        datetime created_at
    }
```

## Observações

* Não há coluna `user_id` em `transactions`: o isolamento do usuário é garantido
  via `account_id → accounts.user_id` (3FN — sem redundância).
* Exclusão de usuário remove suas contas, categorias e metas (`ON DELETE CASCADE`);
  transações são removidas junto da conta. Categorias em uso são protegidas por
  `ON DELETE RESTRICT` — não é possível apagar categoria com transações.
* Categorias possuem `UNIQUE (user_id, name, type)` — impedindo duplicidades.
* Saldos não são persistidos: `saldo = initial_balance + receitas − despesas`,
  calculado sob consulta (consistência garantida com qualquer edição).
