"""Enums de domínio compartilhados entre modelos, schemas e regras de negócio."""

from enum import StrEnum


class TransactionType(StrEnum):
    """Tipo de movimentação financeira (regra de negócio: exclusivos)."""

    RECEITA = "RECEITA"
    DESPESA = "DESPESA"


class CategoryType(StrEnum):
    """Tipo de categoria — deve ser compatível com o tipo da transação."""

    RECEITA = "RECEITA"
    DESPESA = "DESPESA"


class AccountType(StrEnum):
    """Tipos de contas financeiras suportados."""

    CORRENTE = "CORRENTE"
    POUPANCA = "POUPANCA"
    INVESTIMENTO = "INVESTIMENTO"
    ESPECIE = "ESPECIE"
    CARTAO = "CARTAO"
