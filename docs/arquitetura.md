# Arquitetura do Projeto — 5 Centavos

## 1. Objetivo

Este documento descreve a arquitetura planejada para o **5 Centavos**, apresentando a organização dos principais componentes do sistema, suas responsabilidades e a forma como deverão se comunicar.

A arquitetura foi planejada para permitir a evolução gradual do projeto, desde uma aplicação inicial em Python até uma solução composta por banco de dados, API, Analytics, Dashboard e Inteligência Artificial.

---

## 2. Princípios arquiteturais

A arquitetura do 5 Centavos deverá seguir os seguintes princípios:

* Separação de responsabilidades;
* Modularidade;
* Baixo acoplamento entre componentes;
* Facilidade de manutenção;
* Testabilidade;
* Segurança;
* Escalabilidade;
* Evolução incremental;
* Reutilização de componentes;
* Organização do código.

A complexidade da arquitetura deverá aumentar somente conforme as necessidades do projeto.

---

## 3. Arquitetura geral

A arquitetura planejada pode ser representada da seguinte forma:

```text
┌──────────────────────────────┐
│            USUÁRIO           │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       INTERFACE / UI         │
│      Dashboard / Frontend    │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│             API              │
│           FastAPI            │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│      CAMADA DE SERVIÇOS      │
│       Regras de negócio      │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│     CAMADA DE PERSISTÊNCIA   │
│         SQLAlchemy           │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│          BANCO DE DADOS      │
│       SQLite / PostgreSQL    │
└──────────────────────────────┘
```

Os dados armazenados poderão posteriormente alimentar componentes de **Analytics e Inteligência Artificial**.

---

# 4. Camadas do sistema

## 4.1 Interface

A interface será responsável pela interação entre o usuário e o sistema.

Entre suas responsabilidades estarão:

* Exibir informações financeiras;
* Permitir cadastro de receitas e despesas;
* Permitir gerenciamento de contas;
* Exibir saldos;
* Apresentar relatórios;
* Apresentar gráficos;
* Permitir interação com recursos de Analytics;
* Apresentar resultados de Inteligência Artificial.

A tecnologia da interface poderá evoluir durante o projeto.

---

## 4.2 API

A API será responsável por disponibilizar os recursos do sistema para as interfaces e outros consumidores autorizados.

A tecnologia prevista para essa camada é o **FastAPI**.

Exemplos de recursos:

```text
POST   /users
POST   /login

GET    /accounts
POST   /accounts

GET    /transactions
POST   /transactions
PUT    /transactions/{id}
DELETE /transactions/{id}

GET    /reports
GET    /analytics
```

A API deverá receber requisições, validar os dados e encaminhar as operações para as camadas responsáveis.

---

## 4.3 Camada de serviços

A camada de serviços será responsável pela execução das principais regras de negócio da aplicação.

Exemplos:

* Registrar receita;
* Registrar despesa;
* Calcular saldo;
* Validar transações;
* Criar metas;
* Gerar relatórios;
* Processar informações;
* Executar operações financeiras.

Essa camada deverá evitar que as regras de negócio fiquem diretamente dentro da interface ou da API.

---

## 4.4 Camada de persistência

A camada de persistência será responsável pela comunicação entre a aplicação e o banco de dados.

A tecnologia prevista é o **SQLAlchemy**.

Suas responsabilidades incluem:

* Criar registros;
* Consultar registros;
* Atualizar registros;
* Excluir registros;
* Gerenciar relacionamentos;
* Executar operações no banco de dados.

---

## 4.5 Banco de dados

O banco de dados será responsável pelo armazenamento persistente das informações do sistema.

Inicialmente será utilizado **SQLite**, principalmente por sua simplicidade durante o desenvolvimento.

Posteriormente, o projeto deverá evoluir para **PostgreSQL**.

Principais entidades:

```text
USERS
ACCOUNTS
CATEGORIES
TRANSACTIONS
GOALS
```

O modelo detalhado encontra-se em `modelo-de-dados.md`.

---

# 5. Camada de Analytics

A camada de Analytics será responsável por transformar os dados financeiros armazenados em informações úteis.

O processamento poderá utilizar ferramentas como:

* Pandas;
* NumPy;
* SQL;
* Estatística;
* Técnicas de análise exploratória.

Exemplos de análises:

```text
Receitas por mês
Despesas por mês
Gastos por categoria
Evolução do saldo
Média de gastos
Comparação entre períodos
```

Fluxo:

```text
Banco de Dados
      ↓
Extração
      ↓
Tratamento
      ↓
Análise
      ↓
Indicadores
      ↓
Visualizações
```

---

# 6. Dashboard

O Dashboard será responsável pela apresentação visual dos resultados obtidos através dos dados financeiros.

A tecnologia inicialmente prevista é o **Streamlit**, podendo utilizar **Plotly** para geração de gráficos.

Exemplos de informações:

* Saldo atual;
* Receitas;
* Despesas;
* Evolução financeira;
* Gastos por categoria;
* Comparações mensais;
* Metas financeiras;
* Indicadores.

Representação:

```text
┌───────────────────────────────────────┐
│             DASHBOARD                 │
├──────────────┬──────────────┬─────────┤
│ Saldo        │ Receitas     │ Despesas│
├──────────────┴──────────────┴─────────┤
│                                       │
│        Evolução financeira             │
│                                       │
├──────────────────────┬────────────────┤
│ Gastos por categoria │ Metas          │
│                      │                │
└──────────────────────┴────────────────┘
```

---

# 7. Inteligência Artificial

A Inteligência Artificial será incorporada em uma etapa posterior do projeto.

Seu objetivo será utilizar os dados financeiros autorizados para gerar análises e sugestões.

Possíveis aplicações:

* Identificação de padrões de gastos;
* Classificação de transações;
* Detecção de comportamentos;
* Previsões;
* Identificação de anomalias;
* Sugestões personalizadas;
* Análise de hábitos financeiros.

Fluxo planejado:

```text
Dados financeiros
       ↓
Preparação dos dados
       ↓
Processamento
       ↓
Modelo / IA
       ↓
Resultado
       ↓
Usuário
```

Os resultados deverão ser apresentados como **informações e sugestões**, e não como decisões financeiras obrigatórias.

---

# 8. Fluxo completo dos dados

A arquitetura completa poderá funcionar da seguinte maneira:

```text
                  USUÁRIO
                     │
                     ▼
              ┌─────────────┐
              │  INTERFACE  │
              └──────┬──────┘
                     │
                     ▼
              ┌─────────────┐
              │     API     │
              └──────┬──────┘
                     │
                     ▼
              ┌─────────────┐
              │  SERVICES   │
              └──────┬──────┘
                     │
                     ▼
              ┌─────────────┐
              │ REPOSITORY  │
              │ / ORM       │
              └──────┬──────┘
                     │
                     ▼
              ┌─────────────┐
              │  DATABASE   │
              └──────┬──────┘
                     │
            ┌────────┴─────────┐
            ▼                  ▼
       ANALYTICS                IA
            │                  │
            └────────┬─────────┘
                     ▼
                DASHBOARD
                     │
                     ▼
                  USUÁRIO
```

---

# 9. Organização do código

Conforme o projeto evoluir, a estrutura poderá assumir uma organização semelhante a:

```text
5-Centavos/
│
├── docs/
│
├── src/
│   ├── api/
│   ├── models/
│   ├── services/
│   ├── repositories/
│   ├── analytics/
│   ├── ai/
│   └── utils/
│
├── tests/
│
├── data/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── LICENSE
```

Essa estrutura será implementada progressivamente e não deverá ser criada integralmente antes de existir uma necessidade para cada componente.

---

# 10. Segurança

A arquitetura deverá considerar segurança desde as primeiras versões.

Entre as medidas previstas estão:

* Senhas armazenadas utilizando hash;
* Autenticação de usuários;
* Autorização de acesso;
* Isolamento dos dados entre usuários;
* Validação das entradas;
* Proteção das informações financeiras;
* Controle de acesso aos recursos da API.

---

# 11. Testes

Os testes serão incorporados progressivamente ao projeto.

A ferramenta prevista é o **Pytest**.

Os testes poderão abranger:

* Regras de negócio;
* Cálculo de saldo;
* Cadastro de usuários;
* Transações;
* Serviços;
* API;
* Processos de Analytics;
* Funcionalidades de IA.

Fluxo:

```text
Código
  ↓
Teste
  ↓
Validação
  ↓
Correção
  ↓
Novo teste
```

---

# 12. Escalabilidade

A arquitetura deverá permitir a evolução do projeto sem exigir uma reescrita completa da aplicação.

A evolução prevista será:

```text
Aplicação Python
       ↓
SQLite
       ↓
Arquitetura modular
       ↓
PostgreSQL
       ↓
API
       ↓
Analytics
       ↓
Dashboard
       ↓
IA
       ↓
Docker
       ↓
Deploy
```

A adoção de cada tecnologia deverá ocorrer conforme a necessidade da versão correspondente.

---

# 13. Evolução arquitetural

| Versão | Evolução                         |
| ------ | -------------------------------- |
| v0.1.0 | Planejamento e documentação      |
| v0.2.0 | Estrutura inicial em Python      |
| v0.3.0 | Aplicação financeira + SQLite    |
| v0.4.0 | PostgreSQL + arquitetura modular |
| v0.5.0 | API com FastAPI                  |
| v0.6.0 | Analytics                        |
| v0.7.0 | Dashboard                        |
| v0.8.0 | Inteligência Artificial          |
| v1.0.0 | Docker + Deploy                  |

---

# 14. Considerações finais

A arquitetura do **5 Centavos** foi planejada para acompanhar o crescimento do projeto de maneira incremental.

A estrutura inicial deverá permanecer simples, permitindo que os conceitos sejam implementados e compreendidos antes da introdução de novas camadas e tecnologias.

Conforme novas funcionalidades forem adicionadas, a arquitetura poderá ser revisada e documentada.

Alterações arquiteturais relevantes deverão ser registradas no histórico do Git e, quando necessário, neste documento.
