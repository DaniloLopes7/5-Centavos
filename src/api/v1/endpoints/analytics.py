from fastapi import APIRouter, Depends
from typing import List

from src.schemas import FinancialSummary, CategorySummary, MonthlySummary
from src.services import AnalyticsService
from src.api.v1.deps import get_current_user

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/summary", response_model=FinancialSummary)
async def get_financial_summary(current_user: dict = Depends(get_current_user)):
    """Retorna resumo financeiro do usuário."""
    summary = AnalyticsService.get_financial_summary(current_user["id"])
    return FinancialSummary(**summary)


@router.get("/categories", response_model=List[CategorySummary])
async def get_category_summary(current_user: dict = Depends(get_current_user)):
    """Retorna resumo por categorias."""
    categories = AnalyticsService.get_category_summary(current_user["id"])
    return [CategorySummary(**cat) for cat in categories]


@router.get("/monthly", response_model=List[MonthlySummary])
async def get_monthly_summary(current_user: dict = Depends(get_current_user)):
    """Retorna resumo mensal dos últimos 12 meses."""
    months = AnalyticsService.get_monthly_summary(current_user["id"])
    return [MonthlySummary(**month) for month in months]