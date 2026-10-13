"""Schemas da camada de Analytics."""

from decimal import Decimal

from pydantic import BaseModel


class FinancialSummary(BaseModel):
    """Resumo financeiro consolidado de um usuário."""

    total_receitas: Decimal
    total_despesas: Decimal
    saldo_atual: Decimal
    taxa_poupanca: float  # % do que sobrou das receitas
    total_contas: int
    total_transacoes: int
    total_metas: int


class CategoryBreakdownItem(BaseModel):
    """Total agregado por categoria em um período."""

    category: str
    type: str
    total: Decimal
    percentual: float


class MonthlyEvolutionItem(BaseModel):
    """Evolução mês a mês de receitas, despesas e saldo."""

    year_month: str
    receitas: Decimal
    despesas: Decimal
    saldo: Decimal
