"""Serviço de Analytics: indicadores, relatórios e evolução temporal."""

from datetime import date
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from cinco_centavos.models import Account, Goal, Transaction, TransactionType
from cinco_centavos.repositories import AccountRepository, AnalyticsRepository
from cinco_centavos.schemas.analytics import (
    CategoryBreakdownItem,
    FinancialSummary,
    MonthlyEvolutionItem,
)


class AnalyticsService:
    """Análises financeiras do usuário (RF10, RF11, RF12)."""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.analytics = AnalyticsRepository(db)
        self.accounts = AccountRepository(db)

    def get_financial_summary(
        self,
        user_id: int,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> FinancialSummary:
        """Resumo consolidado: receitas, despesas, saldo e taxa de poupança."""
        totals = self.analytics.totals_by_type(user_id, start_date, end_date)
        receitas = totals.get(TransactionType.RECEITA, Decimal(0))
        despesas = totals.get(TransactionType.DESPESA, Decimal(0))

        accounts = self.accounts.list_by_user(user_id)
        nets = self.analytics.account_transaction_totals(user_id)
        saldo_atual = sum(
            (a.initial_balance + nets.get(a.id, Decimal(0)) for a in accounts),
            Decimal(0),
        )

        taxa_poupanca = (
            round(float((receitas - despesas) / receitas) * 100, 2)
            if receitas > 0
            else 0.0
        )

        total_transacoes = self.db.scalar(
            select(func.count(Transaction.id))
            .join(Account, Transaction.account_id == Account.id)
            .where(Account.user_id == user_id)
        ) or 0
        total_metas = self.db.scalar(
            select(func.count(Goal.id)).where(Goal.user_id == user_id)
        ) or 0

        return FinancialSummary(
            total_receitas=receitas,
            total_despesas=despesas,
            saldo_atual=saldo_atual,
            taxa_poupanca=taxa_poupanca,
            total_contas=len(accounts),
            total_transacoes=total_transacoes,
            total_metas=total_metas,
        )

    def get_category_breakdown(
        self,
        user_id: int,
        start_date: date | None = None,
        end_date: date | None = None,
        type: TransactionType | None = None,
    ) -> list[CategoryBreakdownItem]:
        """Totais por categoria com percentual (base de gráficos)."""
        rows = self.analytics.totals_by_category(user_id, start_date, end_date)
        if type is not None:
            rows = [row for row in rows if row[1] == type]
        grand_total = sum((row[2] for row in rows), Decimal(0)) or Decimal(1)
        return [
            CategoryBreakdownItem(
                category=name,
                type=type_.value,
                total=total,
                percentual=round(float(total / grand_total) * 100, 2),
            )
            for name, type_, total in rows
        ]

    def get_monthly_evolution(self, user_id: int) -> list[MonthlyEvolutionItem]:
        """Evolução mensal de receitas, despesas e saldo acumulado."""
        rows = self.analytics.monthly_totals(user_id)

        months: dict[str, MonthlyEvolutionItem] = {}
        for year_month, type_, total in rows:
            item = months.setdefault(
                year_month,
                MonthlyEvolutionItem(
                    year_month=year_month,
                    receitas=Decimal(0),
                    despesas=Decimal(0),
                    saldo=Decimal(0),
                ),
            )
            if type_ == TransactionType.RECEITA:
                months[year_month] = item.model_copy(update={"receitas": total})
            else:
                months[year_month] = item.model_copy(update={"despesas": total})

        saldo_acumulado = Decimal(0)
        result = []
        for month in sorted(months):
            item = months[month]
            saldo_acumulado += item.receitas - item.despesas
            result.append(item.model_copy(update={"saldo": saldo_acumulado}))
        return result
