# Requisitos — 5 Centavos

## 1. Objetivo

Este documento define os requisitos funcionais e não funcionais do 5 Centavos, estabelecendo as funcionalidades esperadas e os critérios de qualidade que deverão orientar o desenvolvimento do projeto.

## 2. Requisitos Funcionais

### RF01 — Cadastro de usuário

O sistema deverá permitir o cadastro de usuários.

### RF02 — Autenticação

O sistema deverá permitir que usuários cadastrados realizem login.

### RF03 — Gerenciamento de contas

O sistema deverá permitir cadastrar, consultar, editar e remover contas financeiras.

### RF04 — Cadastro de receitas

O sistema deverá permitir registrar receitas contendo valor, descrição, categoria, conta e data.

### RF05 — Cadastro de despesas

O sistema deverá permitir registrar despesas contendo valor, descrição, categoria, conta e data.

### RF06 — Gerenciamento de categorias

O sistema deverá permitir criar e gerenciar categorias financeiras.

### RF07 — Consulta de saldo

O sistema deverá calcular e apresentar o saldo das contas financeiras.

### RF08 — Consulta de transações

O sistema deverá permitir consultar as transações financeiras do usuário.

### RF09 — Edição e exclusão de transações

O sistema deverá permitir editar e excluir transações.

### RF10 — Relatórios financeiros

O sistema deverá permitir gerar relatórios sobre receitas, despesas e saldos.

### RF11 — Indicadores financeiros

O sistema deverá apresentar indicadores que auxiliem na compreensão da situação financeira.

### RF12 — Análise de dados

O sistema deverá permitir realizar análises dos dados financeiros utilizando técnicas de Analytics.

### RF13 — Visualização de dados

O sistema deverá apresentar informações financeiras por meio de gráficos e outras visualizações.

### RF14 — Importação de dados

O sistema deverá permitir importar transações por meio de arquivos estruturados, como CSV.

### RF15 — Exportação de dados

O sistema deverá permitir exportar dados financeiros.

### RF16 — Metas financeiras

O sistema deverá permitir criar e acompanhar metas financeiras.

### RF17 — Inteligência Artificial

Em versões futuras, o sistema deverá utilizar Inteligência Artificial para realizar análises e gerar sugestões baseadas nos dados autorizados.

## 3. Requisitos Não Funcionais

### RNF01 — Segurança

O sistema deverá proteger os dados dos usuários e não deverá armazenar senhas em texto puro.

### RNF02 — Privacidade

Cada usuário deverá ter acesso somente aos seus próprios dados financeiros.

### RNF03 — Desempenho

As operações comuns deverão ser realizadas de forma eficiente.

### RNF04 — Manutenibilidade

O código deverá possuir uma estrutura organizada, modular e de fácil manutenção.

### RNF05 — Escalabilidade

A arquitetura deverá permitir a evolução do sistema e a inclusão de novas funcionalidades.

### RNF06 — Testabilidade

As principais funcionalidades deverão possuir testes automatizados.

### RNF07 — Portabilidade

O sistema deverá ser executável em ambientes compatíveis com suas dependências.

### RNF08 — Documentação

As principais funcionalidades, regras de negócio e decisões técnicas deverão ser documentadas.

### RNF09 — Versionamento

O projeto deverá utilizar Git para manter um histórico organizado das alterações.

### RNF10 — Containerização

Em versões futuras, o sistema deverá poder ser executado por meio de containers Docker.

## 4. Priorização

### Alta prioridade

* Cadastro e autenticação;
* Contas financeiras;
* Receitas;
* Despesas;
* Categorias;
* Saldo;
* Transações.

### Média prioridade

* Relatórios;
* Indicadores;
* Metas;
* Importação e exportação;
* Analytics;
* Dashboard.

### Baixa / futura

* Inteligência Artificial;
* Recursos avançados de automação;
* Docker;
* Deploy.

## 5. Evolução

Os requisitos poderão ser refinados conforme novas versões do 5 Centavos forem desenvolvidas.

Alterações relevantes deverão ser documentadas e registradas no histórico do Git.
