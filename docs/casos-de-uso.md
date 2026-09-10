# Casos de Uso — 5 Centavos

## 1. Objetivo

Este documento descreve os principais casos de uso do 5 Centavos, apresentando como os usuários deverão interagir com o sistema para realizar operações financeiras.

## 2. Atores

### Usuário

Pessoa cadastrada que utiliza o 5 Centavos para gerenciar suas informações financeiras.

### Sistema

Responsável por validar dados, executar operações, realizar cálculos e armazenar informações.

### Serviço de Inteligência Artificial

Componente responsável por realizar análises e gerar sugestões baseadas em dados autorizados. Será implementado em versão futura.

## 3. Casos de Uso

### CU01 — Cadastrar usuário

**Ator:** Usuário
**Objetivo:** Criar uma conta no 5 Centavos.

**Pré-condições:**

* O e-mail ainda não pode estar cadastrado.

**Fluxo principal:**

1. Usuário acessa o cadastro.
2. Sistema apresenta o formulário.
3. Usuário informa nome, e-mail e senha.
4. Usuário confirma o cadastro.
5. Sistema valida os dados.
6. Sistema verifica o e-mail.
7. Sistema cria o usuário.
8. Sistema informa o sucesso.

**Fluxos alternativos:**

* E-mail já cadastrado: cadastro rejeitado.
* Campo obrigatório vazio: sistema solicita preenchimento.
* Senha inválida: cadastro rejeitado.

**Pós-condição:** Usuário cadastrado.

### CU02 — Realizar login

**Ator:** Usuário
**Objetivo:** Acessar sua conta.

**Pré-condição:** Usuário cadastrado.

**Fluxo principal:**

1. Usuário informa e-mail e senha.
2. Sistema valida as credenciais.
3. Sistema autentica o usuário.
4. Sistema libera o acesso.

**Fluxo alternativo:** Credenciais inválidas impedem o acesso.

**Pós-condição:** Usuário autenticado.

### CU03 — Cadastrar conta financeira

**Ator:** Usuário
**Objetivo:** Adicionar uma conta financeira.

**Pré-condição:** Usuário autenticado.

**Fluxo principal:**

1. Usuário acessa contas.
2. Seleciona adicionar conta.
3. Informa nome, tipo e saldo inicial.
4. Confirma.
5. Sistema valida e registra a conta.

**Pós-condição:** Conta disponível para o usuário.

### CU04 — Registrar receita

**Ator:** Usuário
**Objetivo:** Registrar uma entrada financeira.

**Pré-condições:**

* Usuário autenticado.
* Conta existente.

**Fluxo principal:**

1. Usuário cria uma nova transação.
2. Seleciona Receita.
3. Informa valor, descrição, categoria, conta e data.
4. Confirma.
5. Sistema valida.
6. Sistema registra a receita.
7. Sistema atualiza o saldo.

**Fluxos alternativos:**

* Valor inválido: operação rejeitada.
* Categoria incompatível: operação rejeitada.
* Conta sem vínculo com o usuário: operação impedida.

**Pós-condição:** Receita registrada e saldo atualizado.

### CU05 — Registrar despesa

**Ator:** Usuário
**Objetivo:** Registrar uma saída financeira.

**Pré-condições:**

* Usuário autenticado.
* Conta existente.

**Fluxo principal:**

1. Usuário cria uma nova transação.
2. Seleciona Despesa.
3. Informa valor, descrição, categoria, conta e data.
4. Confirma.
5. Sistema valida.
6. Sistema registra a despesa.
7. Sistema atualiza o saldo.

**Pós-condição:** Despesa registrada e saldo atualizado.

### CU06 — Consultar saldo

**Ator:** Usuário
**Objetivo:** Visualizar o saldo de uma conta ou o saldo total.

**Pré-condição:** Usuário autenticado.

**Fluxo principal:**

1. Usuário acessa a área financeira.
2. Sistema identifica suas contas.
3. Sistema calcula os saldos.
4. Sistema apresenta os valores.

**Pós-condição:** Saldo atualizado exibido.

### CU07 — Consultar transações

**Ator:** Usuário
**Objetivo:** Visualizar o histórico financeiro.

**Pré-condição:** Usuário autenticado.

**Fluxo principal:**

1. Usuário acessa o histórico.
2. Sistema busca suas transações.
3. Sistema apresenta os registros.
4. Usuário pode aplicar filtros quando disponíveis.

### CU08 — Editar transação

**Ator:** Usuário
**Objetivo:** Alterar uma transação existente.

**Pré-condições:**

* Usuário autenticado.
* Transação pertencente ao usuário.

**Fluxo principal:**

1. Usuário seleciona a transação.
2. Sistema apresenta os dados.
3. Usuário realiza alterações.
4. Usuário confirma.
5. Sistema valida.
6. Sistema atualiza a transação.
7. Sistema recalcula o saldo quando necessário.

### CU09 — Excluir transação

**Ator:** Usuário
**Objetivo:** Remover uma transação.

**Pré-condições:**

* Usuário autenticado.
* Transação pertencente ao usuário.

**Fluxo principal:**

1. Usuário seleciona a transação.
2. Sistema solicita confirmação.
3. Usuário confirma.
4. Sistema remove a transação.
5. Sistema atualiza o saldo.

### CU10 — Gerenciar categorias

**Ator:** Usuário
**Objetivo:** Criar, editar ou excluir categorias.

**Pré-condição:** Usuário autenticado.

**Fluxo principal:**

1. Usuário acessa categorias.
2. Sistema apresenta as categorias.
3. Usuário realiza a operação desejada.
4. Sistema valida.
5. Sistema salva a alteração.

### CU11 — Gerar relatório financeiro

**Ator:** Usuário
**Objetivo:** Obter uma visão consolidada das finanças.

**Pré-condições:**

* Usuário autenticado.
* Dados financeiros disponíveis.

**Fluxo principal:**

1. Usuário acessa relatórios.
2. Seleciona o período.
3. Sistema consulta os dados.
4. Sistema processa as informações.
5. Sistema calcula indicadores.
6. Sistema apresenta o relatório.

### CU12 — Criar meta financeira

**Ator:** Usuário
**Objetivo:** Criar uma meta de economia.

**Pré-condição:** Usuário autenticado.

**Fluxo principal:**

1. Usuário acessa metas.
2. Informa nome, valor-alvo e prazo.
3. Confirma.
4. Sistema valida.
5. Sistema registra a meta.

### CU13 — Importar transações

**Ator:** Usuário
**Objetivo:** Importar transações por arquivo.

**Pré-condições:**

* Usuário autenticado.
* Arquivo em formato compatível.

**Fluxo principal:**

1. Usuário seleciona importação.
2. Seleciona o arquivo.
3. Sistema valida o formato.
4. Sistema processa os registros.
5. Sistema identifica erros.
6. Sistema importa registros válidos.
7. Sistema apresenta o resultado.

### CU14 — Exportar dados financeiros

**Ator:** Usuário
**Objetivo:** Exportar seus dados.

**Pré-condição:** Usuário autenticado.

**Fluxo principal:**

1. Usuário acessa exportação.
2. Seleciona dados e formato.
3. Sistema gera o arquivo.
4. Sistema disponibiliza o arquivo.

### CU15 — Visualizar dashboard

**Ator:** Usuário
**Objetivo:** Visualizar indicadores e gráficos.

**Pré-condições:**

* Usuário autenticado.
* Dados financeiros disponíveis.

**Fluxo principal:**

1. Usuário acessa o dashboard.
2. Sistema coleta os dados.
3. Sistema calcula indicadores.
4. Sistema gera visualizações.
5. Sistema apresenta os resultados.

### CU16 — Realizar análise com Inteligência Artificial

**Atores:** Usuário e Serviço de Inteligência Artificial
**Objetivo:** Obter análises e sugestões baseadas nos dados financeiros.

**Pré-condições:**

* Usuário autenticado.
* Dados suficientes para análise.
* Serviço de IA disponível.

**Fluxo principal:**

1. Usuário solicita uma análise.
2. Sistema seleciona os dados autorizados.
3. Sistema prepara os dados.
4. Sistema envia os dados ao componente de IA.
5. IA realiza a análise.
6. Sistema recebe o resultado.
7. Sistema apresenta a análise.

**Fluxos alternativos:**

* Dados insuficientes: sistema informa o usuário.
* Serviço indisponível: sistema informa que a análise não pôde ser realizada.

## 4. Resumo

| Código | Caso de Uso           | Prioridade |
| ------ | --------------------- | ---------- |
| CU01   | Cadastrar usuário     | Alta       |
| CU02   | Realizar login        | Alta       |
| CU03   | Cadastrar conta       | Alta       |
| CU04   | Registrar receita     | Alta       |
| CU05   | Registrar despesa     | Alta       |
| CU06   | Consultar saldo       | Alta       |
| CU07   | Consultar transações  | Alta       |
| CU08   | Editar transação      | Alta       |
| CU09   | Excluir transação     | Alta       |
| CU10   | Gerenciar categorias  | Alta       |
| CU11   | Gerar relatório       | Média      |
| CU12   | Criar meta financeira | Média      |
| CU13   | Importar transações   | Média      |
| CU14   | Exportar dados        | Média      |
| CU15   | Visualizar dashboard  | Média      |
| CU16   | Análise com IA        | Baixa      |

## 5. Evolução

Os casos de uso serão implementados progressivamente conforme o desenvolvimento do 5 Centavos.

Funcionalidades avançadas, como Analytics, Dashboard e Inteligência Artificial, serão detalhadas e refinadas quando suas respectivas versões forem iniciadas.
