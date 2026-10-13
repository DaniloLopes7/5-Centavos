"""Schemas da camada de Inteligência Artificial."""

from decimal import Decimal

from pydantic import BaseModel, Field


class TrainStatus(BaseModel):
    """Resultado do treinamento dos modelos de IA."""

    status: str
    message: str
    transactions_used: int


class TransactionPredictInput(BaseModel):
    """Entrada para predição de categoria."""

    description: str = Field(min_length=1)
    amount: Decimal = Field(gt=0)
    type: str


class CategoryPrediction(BaseModel):
    """Resultado da predição de categoria de uma transação."""

    category_id: int | None
    category_name: str
    confidence: float


class Anomaly(BaseModel):
    """Transação detectada como anomalia (gasto atípico)."""

    transaction_id: int
    description: str
    amount: Decimal
    date: str
    reason: str


class AnomalyList(BaseModel):
    """Lista de anomalias detectadas."""

    total: int
    anomalies: list[Anomaly]


class CashFlowPrediction(BaseModel):
    """Previsão de fluxo de caixa para os próximos períodos."""

    period_months: int
    expected_receitas: Decimal
    expected_despesas: Decimal
    projected_balance: Decimal
    basis: str  # fatores usados na projeção (transparência)


class InsightsResponse(BaseModel):
    """Insights e sugestões gerados pelo FinancialAdvisor."""

    insights: list[str]
    profile: str | None = None
    cashflow_prediction: CashFlowPrediction | None = None
    anomalies_detected: int = 0
    disclaimer: str = (
        "Sugestões geradas por IA baseadas nos seus dados; "
        "não constituem consultoria financeira obrigatória."
    )
