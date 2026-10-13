"""Repositório de agregações analíticas sobre as transações."""

from datetime import date
from decimal import Decimal

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from cinco_centavos.models import Account, Category, Transaction, TransactionType


class AnalyticsRepository:
    """Consultas de agregação (Analytics) sempre isoladas por usuário."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def _scoped(
        self,
        user_id: int,
        start_date: date | None,
        end_date: date | None,
    ) -> list:
        conditions = [Account.user_id == user_id]
        if start_date is not None:
            conditions.append(Transaction.date >= start_date)
        if end_date is not None:
            conditions.append(Transaction.date <= end_date)
        return conditions

    def totals_by_type(
        self,
        user_id: int,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> dict[TransactionType, Decimal]:
        """Total de receitas e despesas do usuário no período."""
        conditions = self._scoped(user_id, start_date, end_date)
        stmt = (
            select(Transaction.type, func.coalesce(func.sum(Transaction.amount), 0))
            .join(Account, Transaction.account_id == Account.id)
            .where(*conditions)
            .group_by(Transaction.type)
        )
        return {row[0]: Decimal(row[1]) for row in self.db.execute(stmt)}

    def totals_by_category(
        self,
        user_id: int,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[tuple[str, TransactionType, Decimal]]:
        """Total por categoria no período — base para gráficos de pizza/barras."""
        conditions = self._scoped(user_id, start_date, end_date)
        stmt: Select = (
            select(Category.name, Transaction.type, func.sum(Transaction.amount))
            .join(Category, Transaction.category_id == Category.id)
            .join(Account, Transaction.account_id == Account.id)
            .where(*conditions)
            .group_by(Category.name, Transaction.type)
            .order_by(func.sum(Transaction.amount).desc())
        )
        return [
            (row[0], row[1], Decimal(row[2])) for row in self.db.execute(stmt)
        ]

    def monthly_totals(
        self, user_id: int
    ) -> list[tuple[str, TransactionType, Decimal]]:
        """Receitas/despesas agrupadas por ano-mês (evolução temporal)."""
        year_col = func.extract("year", Transaction.date).label("year")
        month_col = func.extract("month", Transaction.date).label("month")
        stmt = (
            select(year_col, month_col, Transaction.type, func.sum(Transaction.amount))
            .join(Account, Transaction.account_id == Account.id)
            .where(Account.user_id == user_id)
            .group_by(year_col, month_col, Transaction.type)
            .order_by(year_col, month_col)
        )
        result = []
        for year, month, type_, total in self.db.execute(stmt):
            result.append((f"{int(year):04d}-{int(month):02d}", type_, Decimal(total)))
        return result

    def account_transaction_totals(self, user_id: int) -> dict[int, Decimal]:
        """Receitas − despesas por conta (usado no cálculo de saldo atual)."""
        receitas = func.coalesce(
            func.sum(Transaction.amount).filter(Transaction.type == TransactionType.RECEITA),
            0,
        )
        despesas = func.coalesce(
            func.sum(Transaction.amount).filter(Transaction.type == TransactionType.DESPESA),
            0,
        )
        stmt = (
            select(Transaction.account_id, (receitas - despesas).label("net"))
            .join(Account, Transaction.account_id == Account.id)
            .where(Account.user_id == user_id)
            .group_by(Transaction.account_id)
        )
        return {row[0]: Decimal(row[1]) for row in self.db.execute(stmt)}
