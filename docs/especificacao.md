# Especificação do Projeto — 5 Centavos

## 1. Identificação

**Nome do projeto:** 5 Centavos
**Tipo:** Plataforma de gerenciamento financeiro pessoal
**Área:** Ciência de Dados, Analytics e Inteligência Artificial
**Versão:** 0.1.0

## 2. Visão geral

O **5 Centavos** é uma plataforma destinada ao gerenciamento de finanças pessoais.

A solução permitirá registrar e organizar informações financeiras e, conforme sua evolução, utilizar esses dados para gerar indicadores, análises, visualizações e recursos de Inteligência Artificial.

O desenvolvimento será realizado de forma incremental, utilizando versões funcionais para demonstrar a evolução técnica e estrutural do projeto.

## 3. Problema

Muitas pessoas possuem dificuldade para acompanhar suas receitas, despesas e hábitos de consumo.

Além de registrar informações financeiras, é importante transformar esses dados em informações que possam auxiliar na compreensão da situação financeira e na tomada de decisões.

O 5 Centavos busca solucionar esse problema centralizando os registros financeiros e utilizando dados para gerar análises relevantes.

## 4. Objetivo geral

Desenvolver uma plataforma de gerenciamento financeiro pessoal capaz de registrar, organizar, processar e analisar dados financeiros, aplicando conceitos de **Ciência de Dados, Analytics e Inteligência Artificial**.

## 5. Objetivos específicos

* Permitir o cadastro de usuários;
* Implementar autenticação;
* Permitir o gerenciamento de contas financeiras;
* Registrar receitas e despesas;
* Organizar transações por categorias;
* Calcular e consultar saldos;
* Gerar relatórios;
* Criar indicadores financeiros;
* Realizar análises de dados;
* Desenvolver dashboards;
* Implementar processos de ETL;
* Explorar aplicações de Inteligência Artificial;
* Implementar testes automatizados;
* Utilizar boas práticas de arquitetura;
* Preparar o projeto para containerização e deploy.

## 6. Público-alvo

O sistema será direcionado principalmente a pessoas que desejam organizar suas finanças pessoais e compreender melhor seus hábitos financeiros através de dados.

## 7. Escopo

### 7.1 Dentro do escopo

* Cadastro de usuários;
* Autenticação;
* Contas financeiras;
* Receitas;
* Despesas;
* Categorias;
* Saldo;
* Histórico de transações;
* Relatórios;
* Indicadores;
* Analytics;
* Dashboard;
* Importação e exportação de dados;
* Metas financeiras;
* Inteligência Artificial;
* Testes;
* Docker;
* Deploy.

### 7.2 Fora do escopo inicial

* Operações bancárias reais;
* Transferências bancárias;
* Acesso direto a contas bancárias;
* Emissão de cartões;
* Consultoria financeira profissional;
* Execução automática de investimentos.

## 8. Arquitetura prevista

A arquitetura será construída e aprimorada conforme as versões do projeto.

```text
Usuário
   ↓
Interface / Dashboard
   ↓
API
   ↓
Camada de Serviços
   ↓
Banco de Dados
   ↓
Analytics / IA
```

A arquitetura poderá ser modificada conforme novas necessidades técnicas forem identificadas.

## 9. Dados principais

O sistema deverá trabalhar inicialmente com as seguintes entidades:

* Usuário;
* Conta financeira;
* Categoria;
* Transação;
* Meta financeira.

## 10. Tecnologias previstas

* Python;
* SQLite;
* PostgreSQL;
* SQLAlchemy;
* FastAPI;
* Pandas;
* NumPy;
* Plotly;
* Streamlit;
* Scikit-learn;
* Pytest;
* Docker.

As tecnologias serão incorporadas progressivamente.

## 11. Evolução do projeto

| Versão | Objetivo                    |
| ------ | --------------------------- |
| v0.1.0 | Planejamento e documentação |
| v0.2.0 | Estrutura inicial em Python |
| v0.3.0 | Sistema financeiro + SQLite |
| v0.4.0 | PostgreSQL + arquitetura    |
| v0.5.0 | API                         |
| v0.6.0 | Analytics                   |
| v0.7.0 | Dashboard                   |
| v0.8.0 | Inteligência Artificial     |
| v1.0.0 | Docker + Deploy             |

## 12. Critérios gerais de sucesso

Cada versão deverá cumprir seus objetivos funcionais, possuir documentação correspondente e manter o código organizado e versionado.

A versão final deverá integrar gerenciamento financeiro, banco de dados, API, Analytics, dashboard, Inteligência Artificial, testes, containerização e deploy.
