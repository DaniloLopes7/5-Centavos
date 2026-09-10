# Roadmap — 5 Centavos

## 1. Objetivo

Este documento apresenta o roadmap de desenvolvimento do **5 Centavos**, organizando a evolução do projeto em etapas e versões.

Cada versão representa um marco de desenvolvimento com objetivos específicos, permitindo acompanhar a evolução da aplicação desde o planejamento inicial até uma solução completa envolvendo gerenciamento financeiro, Banco de Dados, Analytics, Inteligência Artificial, testes, containerização e deploy.

---

# 2. Visão geral

A evolução planejada do projeto é:

```text
v0.1.0
Planejamento e documentação
        ↓
v0.2.0
Estrutura inicial em Python
        ↓
v0.3.0
Sistema financeiro + SQLite
        ↓
v0.4.0
PostgreSQL + arquitetura
        ↓
v0.5.0
API com FastAPI
        ↓
v0.6.0
Analytics
        ↓
v0.7.0
Dashboard
        ↓
v0.8.0
Inteligência Artificial
        ↓
v1.0.0
Docker + Deploy
```

---

# 3. Roadmap de versões

## v0.1.0 — Planejamento e documentação

**Objetivo:** Definir a base conceitual e técnica do projeto.

### Entregas

* Definição do problema;
* Definição dos objetivos;
* Especificação do projeto;
* Requisitos funcionais;
* Requisitos não funcionais;
* Regras de negócio;
* Casos de uso;
* Modelo de dados;
* Diagrama Entidade-Relacionamento;
* Arquitetura inicial;
* README;
* Organização inicial do repositório.

**Status:** 🔄 Em desenvolvimento

---

## v0.2.0 — Estrutura inicial em Python

**Objetivo:** Criar a primeira estrutura executável do projeto.

### Entregas

* Configuração do ambiente Python;
* Organização inicial dos diretórios;
* Criação do ponto de entrada da aplicação;
* Estrutura inicial dos módulos;
* Definição das primeiras classes;
* Configuração inicial de dependências;
* Primeiros testes;
* Execução inicial da aplicação.

**Tecnologias principais:**

* Python;
* Pytest;
* Git.

**Status:** ⏳ Pendente

---

## v0.3.0 — Sistema financeiro + SQLite

**Objetivo:** Criar a primeira versão funcional do gerenciamento financeiro.

### Entregas

* Cadastro de usuários;
* Contas financeiras;
* Categorias;
* Receitas;
* Despesas;
* Transações;
* Consulta de saldo;
* Edição de transações;
* Exclusão de transações;
* Persistência dos dados;
* Banco de dados SQLite;
* Validação das regras de negócio.

**Tecnologias principais:**

* Python;
* SQLite;
* SQL.

**Status:** ⏳ Pendente

---

## v0.4.0 — PostgreSQL + arquitetura

**Objetivo:** Evoluir a estrutura do sistema para uma arquitetura mais organizada e próxima de um ambiente profissional.

### Entregas

* Migração para PostgreSQL;
* Organização em camadas;
* Modelos de dados;
* Repositórios;
* Serviços;
* Configuração de banco de dados;
* SQLAlchemy;
* Melhorias na validação;
* Testes automatizados;
* Separação das responsabilidades.

**Tecnologias principais:**

* PostgreSQL;
* SQLAlchemy;
* Python;
* Pytest.

**Status:** ⏳ Pendente

---

## v0.5.0 — API

**Objetivo:** Disponibilizar os recursos do sistema através de uma API REST.

### Entregas

* Criação da API;
* Endpoints de usuários;
* Autenticação;
* Endpoints de contas;
* Endpoints de categorias;
* Endpoints de transações;
* Endpoints de metas;
* Validação de requisições;
* Tratamento de erros;
* Documentação da API;
* Testes dos endpoints.

**Tecnologias principais:**

* FastAPI;
* Python;
* SQLAlchemy;
* PostgreSQL;
* Pytest.

**Status:** ⏳ Pendente

---

## v0.6.0 — Analytics

**Objetivo:** Transformar os dados financeiros em informações e indicadores úteis.

### Entregas

* Extração dos dados;
* Tratamento dos dados;
* Processos de ETL;
* Análise exploratória;
* Indicadores financeiros;
* Análise de receitas;
* Análise de despesas;
* Análise por categoria;
* Comparações entre períodos;
* Identificação de padrões;
* Preparação dos dados para visualização.

**Tecnologias principais:**

* Python;
* Pandas;
* NumPy;
* SQL;
* Estatística.

**Status:** ⏳ Pendente

---

## v0.7.0 — Dashboard

**Objetivo:** Criar uma interface visual para apresentação dos dados financeiros e indicadores.

### Entregas

* Dashboard financeiro;
* Indicadores principais;
* Gráficos;
* Filtros por período;
* Análise de receitas;
* Análise de despesas;
* Gastos por categoria;
* Evolução do saldo;
* Visualização das metas;
* Integração com Analytics.

**Tecnologias principais:**

* Streamlit;
* Plotly;
* Pandas;
* Python.

**Status:** ⏳ Pendente

---

## v0.8.0 — Inteligência Artificial

**Objetivo:** Aplicar Inteligência Artificial aos dados financeiros de forma responsável.

### Entregas

* Preparação dos dados para IA;
* Classificação de transações;
* Identificação de padrões;
* Detecção de possíveis anomalias;
* Análises automatizadas;
* Previsões quando aplicável;
* Geração de sugestões;
* Integração dos resultados ao sistema;
* Avaliação dos resultados dos modelos.

**Tecnologias possíveis:**

* Scikit-learn;
* Python;
* Pandas;
* Modelos de Machine Learning;
* APIs ou modelos de IA, quando aplicável.

**Status:** ⏳ Pendente

---

## v1.0.0 — Docker + Deploy

**Objetivo:** Preparar o 5 Centavos para execução em um ambiente de produção.

### Entregas

* Dockerfile;
* Docker Compose;
* Containerização da aplicação;
* Configuração de variáveis de ambiente;
* Configuração de produção;
* Banco de dados em ambiente de execução;
* Deploy;
* Documentação de instalação;
* Documentação de execução;
* Revisão de segurança;
* Revisão de testes;
* Preparação da versão estável.

**Tecnologias principais:**

* Docker;
* Docker Compose;
* PostgreSQL;
* GitHub;
* Plataforma de deploy.

**Status:** ⏳ Pendente

---

# 4. Marcos principais

| Versão | Marco        | Resultado                          |
| ------ | ------------ | ---------------------------------- |
| v0.1.0 | Documentação | Projeto planejado                  |
| v0.2.0 | Python       | Estrutura executável               |
| v0.3.0 | SQLite       | Sistema financeiro funcional       |
| v0.4.0 | PostgreSQL   | Arquitetura estruturada            |
| v0.5.0 | API          | Sistema acessível via API          |
| v0.6.0 | Analytics    | Dados transformados em informações |
| v0.7.0 | Dashboard    | Visualização dos indicadores       |
| v0.8.0 | IA           | Recursos inteligentes              |
| v1.0.0 | Deploy       | Aplicação preparada para produção  |

---

# 5. Critérios para conclusão de uma versão

Uma versão será considerada concluída quando:

* Os objetivos definidos para a versão forem implementados;
* As funcionalidades principais estiverem funcionando;
* Os testes necessários forem realizados;
* A documentação estiver atualizada;
* O código estiver versionado no Git;
* As alterações relevantes estiverem registradas;
* O projeto estiver em condição adequada para iniciar a próxima etapa.

Ao concluir uma versão, deverá ser criada uma **tag Git** correspondente.

Exemplo:

```bash
git tag -a v0.3.0 -m "v0.3.0 - Sistema financeiro com SQLite"
```

---

# 6. Estratégia de versionamento

O 5 Centavos será desenvolvido em um único repositório.

Não serão criadas pastas separadas para cada versão.

O histórico das versões será mantido através do **Git**, utilizando commits e tags.

Exemplo:

```text
5-Centavos/
│
├── src/
├── tests/
├── docs/
├── data/
├── main.py
└── README.md
```

As versões anteriores poderão ser consultadas através do histórico do Git.

---

# 7. Atualização do roadmap

O roadmap poderá ser atualizado durante o desenvolvimento caso novas necessidades sejam identificadas.

Alterações poderão incluir:

* Adição de funcionalidades;
* Alteração da ordem das etapas;
* Mudança de tecnologias;
* Criação de novas versões;
* Remoção de funcionalidades que deixarem de fazer sentido.

Alterações relevantes deverão ser registradas e justificadas no histórico do projeto.

---

# 8. Visão de longo prazo

O objetivo final do roadmap é transformar o 5 Centavos em uma aplicação completa que reúna:

```text
Programação
     +
Banco de Dados
     +
Engenharia de Dados
     +
Analytics
     +
Visualização de Dados
     +
Machine Learning
     +
Inteligência Artificial
     +
Testes
     +
Docker
     +
Deploy
```

O projeto deverá demonstrar não apenas a construção de uma aplicação, mas também a utilização de dados para gerar informações e apoiar decisões.

---

# 9. Status atual

**Versão atual:** v0.1.0

**Etapa:** Planejamento e documentação

**Próxima versão:** v0.2.0 — Estrutura inicial em Python

**Situação:** ✅ Finalizado
