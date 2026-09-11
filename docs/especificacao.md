# Especificação do Projeto — 5 Centavos

## 1. Identificação

**Nome do projeto:** 5 Centavos
**Tipo:** Gestão financeira pessoal
**Área:** Ciência de Dados, Analytics e IA
**Versão:** 0.3.0

## 2. Visão geral

O **5 Centavos** serve para organizar finanças pessoais. O sistema permite registrar receitas, despesas e organizar dados para gerar indicadores e análises futuras, incluindo recursos de IA.

O desenvolvimento é incremental, com versões funcionais para acompanhar a evolução técnica.

## 3. Problema

A dificuldade de acompanhar receitas, despesas e hábitos de consumo. O projeto busca centralizar esses registros e transformá-los em informações úteis para a tomada de decisão.

## 4. Objetivo geral

Criar uma plataforma de gestão financeira capaz de registrar, processar e analisar dados, aplicando conceitos de Ciência de Dados e IA.

## 5. Objetivos específicos

* Cadastro de usuários e autenticação;
* Gestão de contas financeiras;
* Registro de receitas e despesas categorizadas;
* Cálculo de saldos;
* Geração de relatórios e indicadores;
* Desenvolvimento de dashboards e processos de ETL;
* Implementação de IA;
* Testes automatizados e boas práticas de arquitetura;
* Containerização e deploy.

## 6. Público-alvo

Pessoas que querem organizar suas finanças e entender seus hábitos através de dados.

## 7. Escopo

### 7.1 No escopo
* Cadastro, autenticação e gestão de contas;
* Receitas, despesas e categorias;
* Saldo e histórico de transações;
* Relatórios, indicadores, Analytics e Dashboard;
* Importação/Exportação de dados e metas financeiras;
* IA, Testes, Docker e Deploy.

### 7.2 Fora do escopo
* Operações bancárias reais ou transferências;
* Acesso direto a APIs bancárias;
* Consultoria financeira profissional.

## 8. Arquitetura prevista

A arquitetura evolui com as versões:

```text
Usuário -> Interface/Dashboard -> API -> Serviços -> Banco de Dados -> Analytics/IA
```

## 9. Entidades principais

* Usuário;
* Conta financeira;
* Categoria;
* Transação;
* Meta financeira.

## 10. Tecnologias

* Python, SQLite, PostgreSQL, SQLAlchemy, FastAPI, Pandas, NumPy, Plotly, Streamlit, Scikit-learn, Pytest, Docker.

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

## 12. Sucesso do projeto

Cada versão deve cumprir seus objetivos funcionais, ter documentação atualizada e código versionado. O resultado final deve integrar todas as camadas (Financeiro -> Banco -> API -> Analytics -> Dashboard -> IA -> Deploy).
