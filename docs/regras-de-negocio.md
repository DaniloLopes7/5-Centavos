# Regras de Negócio — 5 Centavos

## 1. Objetivo

Regras para garantir a consistência e integridade dos dados financeiros.

## 2. Usuários

* **Cadastro único:** Cada usuário deve ter apenas um cadastro.
* **E-mail único:** O e-mail deve ser exclusivo para cada conta.
* **Privacidade:** Usuários acessam apenas seus próprios dados.
* **Autenticação:** Operações financeiras exigem login.
* **Segurança:** Senhas armazenadas via hash, nunca em texto puro.

## 3. Contas Financeiras

* **Vínculo:** Toda conta deve pertencer a um único usuário.
* **Identificação:** Contas devem ter um nome identificador.
* **Saldo Inicial:** Permite-se a definição de um saldo inicial no cadastro.
* **Isolamento:** Proibido acessar contas de outros usuários.

## 4. Transações

* **Vínculo:** Transações devem estar ligadas a uma conta existente.
* **Valor:** O valor deve ser obrigatoriamente maior que zero.
* **Tipo:** Classificadas estritamente como Receita ou Despesa.
* **Impacto no Saldo:** Receitas aumentam e despesas diminuem o saldo da conta.
* **Data:** Toda transação deve ter data válida.
* **Categoria:** Devem ter categoria compatível com o tipo da transação.
* **Integridade:** Proibido vincular a contas ou categorias inexistentes ou de terceiros.

## 5. Categorias

* **Vínculo:** Categorias pertencem a um usuário.
* **Tipo:** Devem ser classificadas para receitas ou despesas.
* **Compatibilidade:** Bloquear uso de categoria de receita em transação de despesa (e vice-versa).

## 6. Saldo

* **Cálculo:** Saldo = Saldo Inicial + Receitas - Despesas.
* **Atualização:** Qualquer alteração em transações deve refletir no saldo.

## 7. Metas Financeiras

* **Vínculo:** Metas pertencem a um usuário.
* **Valor-alvo:** Deve ser maior que zero.
* **Prazo:** Opcional.
* **Progresso:** Calculado com base no valor acumulado vs valor-alvo.

## 8. Importação e Exportação

* **Formato:** Devem seguir o padrão definido pelo sistema.
* **Validação:** Registros inválidos são descartados na importação.
* **Acesso:** Exportação limitada aos dados do próprio usuário.

## 9. Analytics e IA

* **Qualidade:** Dados validados antes de análises.
* **Autorização:** Indicadores usam apenas dados do usuário.
* **Períodos:** Análises baseadas em intervalos definidos pelo usuário.
* **IA:** Sugestões da IA não são decisões financeiras obrigatórias.
* **Transparência:** Indicar fatores usados na análise da IA.

## 10. Integridade e Segurança

* **Referências:** Evitar registros órfãos (sem referências válidas).
* **Consistência:** Impedir operações que gerem dados inconsistentes.
* **Isolamento:** Bloquear qualquer acesso indevido entre usuários.
