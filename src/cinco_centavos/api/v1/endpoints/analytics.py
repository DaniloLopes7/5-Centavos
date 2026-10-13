"""Endpoints de Analytics (RF10, RF11, RF12)."""

from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from cinco_centavos.api.v1.deps import get_current_user
from cinco_centavos.core.database import get_db
from cinco_centavos.models import TransactionType, User
from cinco_centavos.schemas import (
    CategoryBreakdownItem,
    FinancialSummary,
    MonthlyEvolutionItem,
)
from cinco_centavos.services import AnalyticsService

router = APIRouter(
    prefix="/analytics", tags=["Analytics"], dependencies=[Depends(get_current_user)]
)


@router.get("/summary", response_model=FinancialSummary, summary="Resumo financeiro")
def summary(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> FinancialSummary:
    return AnalyticsService(db).get_financial_summary(
        current_user.id, start_date, end_date
    )


@router.get(
    "/categories",
    response_model=list[CategoryBreakdownItem],
    summary="Totais por categoria",
)
def categories(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    type: TransactionType | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[CategoryBreakdownItem]:
    return AnalyticsService(db).get_category_breakdown(
        current_user.id, start_date, end_date, type
    )


@router.get(
    "/monthly",
    response_model=list[MonthlyEvolutionItem],
    summary="Evolução mensal",
)
def monthly(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> list[MonthlyEvolutionItem]:
    return AnalyticsService(db).get_monthly_evolution(current_user.id)
