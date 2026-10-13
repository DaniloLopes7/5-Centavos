# Regras de Negócio — 5 Centavos

## 1. Objetivo

Regras para garantir a consistência e integridade dos dados financeiros.

## 2. Usuários

* **Cadastro único:** Cada usuário deve ter apenas um cadastro.
* **E-mail único:** O e-mail deve ser exclusivo para cada conta (HTTP 409 em duplicidade).
* **Privacidade:** Usuários acessam apenas seus próprios dados.
* **Autenticação:** Operações financeiras exigem login (JWT Bearer).
* **Segurança:** Senhas armazenadas via hash bcrypt, nunca em texto puro.
* **Categorias padrão:** Todo novo usuário recebe categorias básicas de receita e despesa.

## 3. Contas Financeiras

* **Vínculo:** Toda conta deve pertencer a um único usuário.
* **Identificação:** Contas devem ter um nome identificador.
* **Tipos válidos:** `CORRENTE`, `POUPANCA`, `INVESTIMENTO`, `ESPECIE`, `CARTAO`.
* **Saldo Inicial:** Permite-se a definição de um saldo inicial no cadastro.
* **Isolamento:** Proibido acessar contas de outros usuários.

## 4. Transações

* **Vínculo:** Transações devem estar ligadas a uma conta existente.
* **Valor:** O valor deve ser obrigatoriamente maior que zero (validado na API — `amount > 0` — e no banco via `CHECK`).
* **Tipo:** Classificadas estritamente como `RECEITA` ou `DESPESA`.
* **Impacto no Saldo:** Receitas aumentam e despesas diminuem o saldo da conta.
* **Data:** Toda transação deve ter data válida (permitidas datas passadas e futuras).
* **Categoria:** Devem ter categoria compatível com o tipo da transação.
* **Integridade:** Proibido vincular a contas ou categorias inexistentes ou de terceiros.

## 5. Categorias

* **Vínculo:** Categorias pertencem a um usuário.
* **Tipo:** Devem ser classificadas para receitas ou despesas.
* **Unicidade:** Não pode haver duas categorias com mesmo nome e tipo para o mesmo usuário.
* **Compatibilidade:** Bloquear uso de categoria de receita em transação de despesa (e vice-versa).
* **Exclusão:** Categorias em uso por transações não são removidas (FK `RESTRICT`).

## 6. Saldo

* **Cálculo:** `Saldo = Saldo Inicial + Receitas − Despesas`.
* **Atualização:** Qualquer alteração em transações deve refletir no saldo (cálculo sob consulta, sem persistência de valor derivado).

## 7. Metas Financeiras

* **Vínculo:** Metas pertencem a um usuário.
* **Valor-alvo:** Deve ser maior que zero.
* **Valor acumulado:** Não pode ser negativo; evolui via endpoint de progresso.
* **Prazo:** Opcional.
* **Progresso:** Calculado com base no valor acumulado vs valor-alvo.

## 8. Importação e Exportação

* **Formato:** CSVs devem seguir o padrão definido em `data/` (ver `etl/load_data.py`).
* **Validação:** Registros inválidos são descartados na importação e contabilizados no relatório.
* **Idempotência:** Executar o ETL duas vezes não duplica usuários, contas, categorias, metas ou transações.
* **Acesso:** Exportação (RF15, planejada) será limitada aos dados do próprio usuário.

## 9. Analytics e IA

* **Qualidade:** Dados validados antes de análises.
* **Autorização:** Indicadores usam apenas dados do usuário autenticado.
* **Períodos:** Análises baseadas em intervalos definidos pelo usuário.
* **Mínimo de dados:** Modelos de IA exigem ao menos 8 transações do usuário; abaixo disso respondem de forma graciosa (sem predições).
* **IA:** Sugestões da IA não são decisões financeiras obrigatórias.
* **Transparência:** Toda resposta de IA indica os fatores usados na análise (campo `basis`/justificativa).

## 10. Integridade e Segurança

* **Referências:** Evitar registros órfãos (FKs com `CASCADE`/`RESTRICT` apropriados).
* **Consistência:** Impedir operações que gerem dados inconsistentes (camada de serviços).
* **Isolamento:** Bloquear qualquer acesso indevido entre usuários (filtro obrigatório por `user_id`).
* **Rate limiting:** Endpoints de autenticação limitados por IP.
