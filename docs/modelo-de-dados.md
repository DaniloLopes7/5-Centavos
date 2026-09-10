# Modelo de Dados — 5 Centavos

## 1. Objetivo

Este documento apresenta o modelo de dados inicial do **5 Centavos**, definindo as principais entidades, seus atributos, relacionamentos e regras de integridade que deverão orientar a implementação do banco de dados.

O modelo foi desenvolvido considerando as funcionalidades previstas para o gerenciamento financeiro pessoal e a futura utilização dos dados em processos de **Analytics, Engenharia de Dados e Inteligência Artificial**.

---

## 2. Visão geral

O banco de dados deverá armazenar informações relacionadas a:

* Usuários;
* Contas financeiras;
* Categorias;
* Transações;
* Metas financeiras.

As entidades deverão ser relacionadas de forma a garantir a integridade dos dados e o isolamento das informações financeiras de cada usuário.

### Relacionamento geral

```text
USUÁRIO
   │
   ├───────────────┐
   │               │
   ▼               ▼
CONTAS          METAS
   │
   ▼
TRANSAÇÕES
   │
   ▼
CATEGORIAS
```

---

# 3. Entidades

## 3.1 Usuário

Representa a pessoa cadastrada no sistema.

### Tabela: `users`

| Campo           | Tipo previsto | Restrições       | Descrição                          |
| --------------- | ------------- | ---------------- | ---------------------------------- |
| `id`            | INTEGER       | PK               | Identificador único do usuário     |
| `name`          | VARCHAR       | NOT NULL         | Nome do usuário                    |
| `email`         | VARCHAR       | NOT NULL, UNIQUE | E-mail do usuário                  |
| `password_hash` | VARCHAR       | NOT NULL         | Senha armazenada em formato seguro |
| `created_at`    | DATETIME      | NOT NULL         | Data de criação do cadastro        |

### Regras

* Cada usuário deverá possuir um identificador único.
* O e-mail deverá ser único.
* A senha não deverá ser armazenada em texto puro.
* O usuário somente poderá acessar seus próprios dados.

---

## 3.2 Conta financeira

Representa uma conta ou carteira utilizada pelo usuário para controlar seus recursos financeiros.

Exemplos:

* Conta corrente;
* Conta poupança;
* Carteira;
* Conta digital;
* Dinheiro em espécie.

### Tabela: `accounts`

| Campo             | Tipo previsto | Restrições   | Descrição              |
| ----------------- | ------------- | ------------ | ---------------------- |
| `id`              | INTEGER       | PK           | Identificador da conta |
| `user_id`         | INTEGER       | FK, NOT NULL | Usuário proprietário   |
| `name`            | VARCHAR       | NOT NULL     | Nome da conta          |
| `type`            | VARCHAR       | NOT NULL     | Tipo da conta          |
| `initial_balance` | DECIMAL       | NOT NULL     | Saldo inicial          |
| `created_at`      | DATETIME      | NOT NULL     | Data de criação        |

### Relacionamento

```text
USUÁRIO 1 ───────── N CONTAS
```

Um usuário pode possuir várias contas, enquanto cada conta pertence a apenas um usuário.

---

## 3.3 Categoria

Representa a classificação utilizada para organizar as transações financeiras.

Exemplos:

**Despesas**

* Alimentação;
* Transporte;
* Moradia;
* Lazer;
* Educação.

**Receitas**

* Salário;
* Freelance;
* Investimentos;
* Outros.

### Tabela: `categories`

| Campo     | Tipo previsto | Restrições   | Descrição                  |
| --------- | ------------- | ------------ | -------------------------- |
| `id`      | INTEGER       | PK           | Identificador da categoria |
| `user_id` | INTEGER       | FK, NOT NULL | Usuário proprietário       |
| `name`    | VARCHAR       | NOT NULL     | Nome da categoria          |
| `type`    | VARCHAR       | NOT NULL     | Tipo da categoria          |

### Relacionamento

```text
USUÁRIO 1 ───────── N CATEGORIAS
```

Cada categoria pertence a um usuário.

---

## 3.4 Transação

Representa uma movimentação financeira registrada no sistema.

Uma transação pode ser uma **Receita** ou uma **Despesa**.

### Tabela: `transactions`

| Campo         | Tipo previsto | Restrições   | Descrição                  |
| ------------- | ------------- | ------------ | -------------------------- |
| `id`          | INTEGER       | PK           | Identificador da transação |
| `account_id`  | INTEGER       | FK, NOT NULL | Conta associada            |
| `category_id` | INTEGER       | FK, NOT NULL | Categoria associada        |
| `description` | VARCHAR       | NOT NULL     | Descrição da movimentação  |
| `amount`      | DECIMAL       | NOT NULL     | Valor da transação         |
| `type`        | VARCHAR       | NOT NULL     | Receita ou Despesa         |
| `date`        | DATE          | NOT NULL     | Data da movimentação       |
| `created_at`  | DATETIME      | NOT NULL     | Data de registro           |

### Relacionamentos

```text
CONTA 1 ───────── N TRANSAÇÕES

CATEGORIA 1 ───── N TRANSAÇÕES
```

Uma conta pode possuir diversas transações.

Uma categoria também pode estar associada a diversas transações.

---

## 3.5 Meta financeira

Representa um objetivo financeiro definido pelo usuário.

Exemplos:

* Economizar R$ 5.000;
* Comprar um computador;
* Criar reserva de emergência;
* Fazer uma viagem.

### Tabela: `goals`

| Campo            | Tipo previsto | Restrições   | Descrição             |
| ---------------- | ------------- | ------------ | --------------------- |
| `id`             | INTEGER       | PK           | Identificador da meta |
| `user_id`        | INTEGER       | FK, NOT NULL | Usuário proprietário  |
| `name`           | VARCHAR       | NOT NULL     | Nome da meta          |
| `target_amount`  | DECIMAL       | NOT NULL     | Valor-alvo            |
| `current_amount` | DECIMAL       | NOT NULL     | Valor acumulado       |
| `deadline`       | DATE          | NULL         | Data limite           |
| `created_at`     | DATETIME      | NOT NULL     | Data de criação       |

### Relacionamento

```text
USUÁRIO 1 ───────── N METAS
```

Um usuário pode possuir várias metas financeiras.

---

# 4. Relacionamentos

O modelo inicial possui os seguintes relacionamentos:

| Origem    | Relação | Destino    |
| --------- | ------- | ---------- |
| Usuário   | 1:N     | Contas     |
| Usuário   | 1:N     | Categorias |
| Usuário   | 1:N     | Metas      |
| Conta     | 1:N     | Transações |
| Categoria | 1:N     | Transações |

### Modelo conceitual

```text
                    ┌──────────────┐
                    │    USERS     │
                    ├──────────────┤
                    │ PK id        │
                    │ name         │
                    │ email        │
                    │ password_hash│
                    │ created_at   │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              │ 1:N        │ 1:N        │ 1:N
              ▼            ▼            ▼
       ┌────────────┐ ┌────────────┐ ┌────────────┐
       │  ACCOUNTS  │ │ CATEGORIES │ │   GOALS    │
       ├────────────┤ ├────────────┤ ├────────────┤
       │ PK id      │ │ PK id      │ │ PK id      │
       │ FK user_id │ │ FK user_id │ │ FK user_id │
       │ name       │ │ name       │ │ name       │
       │ type       │ │ type       │ │ target     │
       │ balance    │ │            │ │ current    │
       └──────┬─────┘ └──────┬─────┘ │ deadline   │
              │              │       └────────────┘
              │ 1:N          │ 1:N
              └──────┬───────┘
                     ▼
              ┌──────────────┐
              │ TRANSACTIONS │
              ├──────────────┤
              │ PK id        │
              │ FK account_id│
              │ FK category_id
              │ description  │
              │ amount       │
              │ type         │
              │ date         │
              │ created_at   │
              └──────────────┘
```

---

# 5. Chaves primárias

Cada entidade deverá possuir uma chave primária (`PK`) responsável por identificar exclusivamente cada registro.

| Tabela         | Chave primária |
| -------------- | -------------- |
| `users`        | `id`           |
| `accounts`     | `id`           |
| `categories`   | `id`           |
| `transactions` | `id`           |
| `goals`        | `id`           |

---

# 6. Chaves estrangeiras

As chaves estrangeiras (`FK`) serão utilizadas para estabelecer os relacionamentos entre as entidades.

| Tabela         | Campo         | Referência      |
| -------------- | ------------- | --------------- |
| `accounts`     | `user_id`     | `users.id`      |
| `categories`   | `user_id`     | `users.id`      |
| `transactions` | `account_id`  | `accounts.id`   |
| `transactions` | `category_id` | `categories.id` |
| `goals`        | `user_id`     | `users.id`      |

---

# 7. Integridade dos dados

O banco deverá respeitar as seguintes condições:

* Uma conta deverá pertencer a um usuário existente.
* Uma categoria deverá pertencer a um usuário existente.
* Uma meta deverá pertencer a um usuário existente.
* Uma transação deverá estar vinculada a uma conta existente.
* Uma transação deverá estar vinculada a uma categoria existente.
* Valores financeiros deverão ser maiores que zero quando aplicável.
* O tipo da transação deverá ser `RECEITA` ou `DESPESA`.
* O tipo da categoria deverá ser compatível com a transação.
* Usuários não poderão acessar registros pertencentes a outros usuários.

---

# 8. Cálculo do saldo

O saldo de uma conta deverá considerar o saldo inicial e as movimentações registradas.

A fórmula conceitual será:

```text
Saldo = Saldo Inicial + Receitas - Despesas
```

Exemplo:

```text
Saldo inicial = R$ 1.000,00
Receitas      = R$ 2.000,00
Despesas      = R$   750,00

Saldo atual   = R$ 2.250,00
```

O cálculo poderá ser realizado pela aplicação ou por consultas ao banco, dependendo da arquitetura adotada durante o desenvolvimento.

---

# 9. Valores monetários

Valores financeiros deverão utilizar um tipo numérico adequado para representar valores monetários, evitando o uso de tipos de ponto flutuante para operações financeiras críticas.

A implementação deverá utilizar `DECIMAL`/`NUMERIC` no banco de dados quando suportado.

---

# 10. Normalização

O modelo deverá seguir princípios de normalização para reduzir redundância e inconsistência dos dados.

A estrutura inicial deverá buscar atender, no mínimo, à **Terceira Forma Normal (3FN)**.

As informações deverão ser armazenadas em entidades específicas, evitando duplicação desnecessária.

Por exemplo, o nome da categoria não deverá ser repetido diretamente em cada transação. A transação deverá armazenar a referência para a categoria através de `category_id`.

---

# 11. Evolução futura

O modelo poderá ser expandido conforme novas funcionalidades sejam implementadas.

Possíveis entidades futuras:

* `budgets` — orçamentos financeiros;
* `recurring_transactions` — transações recorrentes;
* `attachments` — anexos de comprovantes;
* `notifications` — notificações;
* `audit_logs` — registros de auditoria;
* `imports` — controle de importações;
* `ai_insights` — análises e recomendações geradas por IA.

Essas entidades somente deverão ser adicionadas quando houver uma necessidade funcional definida.

---

# 12. Relação com Analytics e Ciência de Dados

O modelo foi estruturado considerando que os dados financeiros poderão posteriormente alimentar processos de **ETL, Analytics e Inteligência Artificial**.

As transações serão uma das principais fontes de dados analíticos.

A partir delas, poderão ser calculados indicadores como:

* Total de receitas por período;
* Total de despesas por período;
* Despesas por categoria;
* Evolução do saldo;
* Média de gastos;
* Comparação entre períodos;
* Percentual de gastos por categoria;
* Evolução das metas;
* Identificação de padrões de consumo.

Em versões futuras, esses dados poderão ser utilizados para modelos estatísticos e de Machine Learning.

---

# 13. Tecnologias previstas

A implementação do modelo deverá evoluir conforme as versões do projeto.

| Versão  | Tecnologia         |
| ------- | ------------------ |
| V0.3.0  | SQLite             |
| V0.4.0  | PostgreSQL         |
| V0.4.0+ | SQLAlchemy         |
| V0.5.0+ | API com FastAPI    |
| V0.6.0+ | Pandas e Analytics |

---

# 14. Considerações finais

Este modelo representa a estrutura inicial de dados do **5 Centavos**.

Ele deverá servir como referência para a implementação do banco de dados e poderá ser revisado conforme novas necessidades forem identificadas durante o desenvolvimento.

Alterações estruturais relevantes deverão ser documentadas e registradas no histórico de versionamento do Git.
