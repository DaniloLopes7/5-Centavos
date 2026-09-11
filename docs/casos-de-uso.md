# Casos de Uso — 5 Centavos

## 1. Objetivo

Descrição das interações do usuário com o sistema para realizar operações financeiras.

## 2. Atores

* **Usuário:** Pessoa que gerencia suas finanças.
* **Sistema:** Valida dados, processa cálculos e armazena informações.
* **IA (Futuro):** Gera análises e sugestões.

## 3. Operações

### CU01 — Cadastrar usuário
1. Usuário informa nome, e-mail e senha.
2. Sistema valida e-mail único e dados obrigatórios.
3. Sistema cria a conta.

### CU02 — Realizar login
1. Usuário informa e-mail e senha.
2. Sistema valida credenciais.
3. Sistema libera o acesso.

### CU03 — Cadastrar conta financeira
1. Usuário informa nome, tipo e saldo inicial.
2. Sistema valida e registra a conta vinculada ao usuário.

### CU04 — Registrar receita
1. Usuário seleciona a conta e a categoria.
2. Informa valor, descrição e data.
3. Sistema registra a entrada e aumenta o saldo da conta.

### CU05 — Registrar despesa
1. Usuário seleciona a conta e a categoria.
2. Informa valor, descrição e data.
3. Sistema registra a saída e diminui o saldo da conta.

### CU06 — Consultar saldo
1. Usuário acessa a área financeira.
2. Sistema calcula e exibe o saldo atual das contas.

### CU07 — Consultar transações
1. Usuário acessa o histórico.
2. Sistema lista as transações da conta selecionada.

### CU08 — Editar transação
1. Usuário seleciona a transação e altera os dados.
2. Sistema valida e atualiza o registro e o saldo da conta.

### CU09 — Excluir transação
1. Usuário seleciona a transação e confirma a exclusão.
2. Sistema remove o registro e recalcula o saldo.

### CU10 — Gerenciar categorias
1. Usuário cria ou edita categorias de receita/despesa.
2. Sistema valida e salva as alterações.

### CU11 — Gerar relatório
1. Usuário define o período de análise.
2. Sistema processa os dados e exibe indicadores consolidados.

### CU12 — Criar meta financeira
1. Usuário define nome, valor-alvo e prazo.
2. Sistema registra a meta para acompanhamento.

### CU13 — Importar transações
1. Usuário fornece arquivo CSV.
2. Sistema valida o formato e importa os registros válidos.

### CU14 — Exportar dados
1. Usuário seleciona os dados e o formato.
2. Sistema gera o arquivo para download.

### CU15 — Visualizar dashboard
1. Usuário acessa o dashboard.
2. Sistema gera gráficos e indicadores em tempo real.

### CU16 — Análise com IA (Futuro)
1. Usuário solicita análise de gastos.
2. Sistema processa os dados via IA e apresenta sugestões.

## 4. Prioridades

| Prioridade | Casos de Uso |
| ---------- | ------------ |
| Alta       | CU01 a CU10   |
| Média      | CU11 a CU15   |
| Baixa      | CU16          |
