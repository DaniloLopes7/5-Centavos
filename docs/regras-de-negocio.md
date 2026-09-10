# Regras de Negócio — 5 Centavos

## 1. Objetivo

Este documento define as regras que determinam o comportamento e as condições que deverão ser respeitadas pelo 5 Centavos para garantir a consistência, segurança e integridade dos dados financeiros.

## 2. Usuários

### RN01 — Cadastro único

Cada usuário deverá possuir um cadastro único no sistema.

### RN02 — E-mail único

O e-mail utilizado no cadastro deverá ser único.

### RN03 — Acesso aos dados

Um usuário somente poderá visualizar, criar, alterar ou excluir informações pertencentes à sua própria conta.

### RN04 — Autenticação

Operações que envolvam dados financeiros deverão ser realizadas por usuários autenticados.

### RN05 — Segurança da senha

As senhas não deverão ser armazenadas em texto puro e deverão utilizar mecanismo adequado de hash.

## 3. Contas financeiras

### RN06 — Associação da conta

Toda conta financeira deverá estar associada a um único usuário.

### RN07 — Identificação da conta

Toda conta deverá possuir um nome para identificação.

### RN08 — Saldo inicial

Uma conta poderá possuir um saldo inicial informado pelo usuário.

### RN09 — Isolamento das contas

Um usuário não poderá acessar, alterar ou excluir contas pertencentes a outro usuário.

## 4. Transações

### RN10 — Associação da transação

Toda transação deverá estar vinculada a uma conta financeira existente.

### RN11 — Valor válido

O valor de uma transação deverá ser maior que zero.

### RN12 — Tipo de transação

Toda transação deverá ser classificada como Receita ou Despesa.

### RN13 — Receita

Uma receita deverá aumentar o saldo da conta associada.

### RN14 — Despesa

Uma despesa deverá diminuir o saldo da conta associada.

### RN15 — Data da transação

Toda transação deverá possuir uma data válida.

### RN16 — Categoria

Toda transação deverá possuir uma categoria compatível com seu tipo.

### RN17 — Integridade

Uma transação não poderá ser vinculada a uma conta ou categoria inexistente ou pertencente a outro usuário.

## 5. Categorias

### RN18 — Associação da categoria

Cada categoria deverá estar associada a um usuário.

### RN19 — Tipo da categoria

A categoria deverá indicar se é destinada a receitas, despesas ou, caso seja definido futuramente, a ambos.

### RN20 — Compatibilidade

Uma transação não poderá utilizar uma categoria incompatível com seu tipo.

## 6. Saldo

### RN21 — Cálculo do saldo

O saldo deverá considerar o saldo inicial, as receitas e as despesas da conta.

### RN22 — Fórmula do saldo

```text
Saldo = Saldo Inicial + Receitas - Despesas
```

### RN23 — Atualização do saldo

A inclusão, alteração ou exclusão de uma transação deverá refletir corretamente no saldo da conta.

## 7. Metas financeiras

### RN24 — Associação da meta

Toda meta deverá estar associada a um único usuário.

### RN25 — Valor-alvo

O valor-alvo deverá ser maior que zero.

### RN26 — Prazo

A meta poderá possuir uma data limite.

### RN27 — Progresso

O progresso deverá considerar o valor acumulado em relação ao valor-alvo.

## 8. Importação e exportação

### RN28 — Formato de importação

Os arquivos importados deverão seguir o formato definido pelo sistema.

### RN29 — Validação da importação

Registros inválidos deverão ser identificados antes de serem inseridos.

### RN30 — Exportação

O usuário somente poderá exportar dados financeiros aos quais possui acesso.

## 9. Analytics

### RN31 — Qualidade dos dados

Os dados utilizados nas análises deverão ser previamente validados e processados.

### RN32 — Indicadores

Os indicadores deverão utilizar somente dados autorizados do usuário.

### RN33 — Período de análise

As análises poderão considerar períodos definidos pelo usuário.

## 10. Inteligência Artificial

### RN34 — Dados autorizados

Os recursos de Inteligência Artificial deverão utilizar somente dados autorizados e disponíveis para análise.

### RN35 — Recomendações

As recomendações geradas pela IA deverão ser apresentadas como sugestões e não como decisões financeiras obrigatórias.

### RN36 — Transparência

Sempre que possível, o sistema deverá apresentar os principais fatores utilizados para gerar uma análise ou recomendação.

## 11. Integridade e segurança

### RN37 — Integridade referencial

O sistema deverá evitar registros financeiros sem referências válidas.

### RN38 — Consistência

Operações que produzam dados inconsistentes deverão ser impedidas.

### RN39 — Isolamento dos usuários

Nenhuma operação poderá permitir acesso indevido aos dados de outro usuário.

### RN40 — Auditoria

Operações relevantes poderão ser registradas futuramente para permitir o acompanhamento das alterações realizadas no sistema.

## 12. Evolução das regras

As regras de negócio poderão ser adicionadas, alteradas ou removidas conforme o projeto evoluir.

Alterações relevantes deverão ser documentadas e registradas no histórico de versionamento do Git.
