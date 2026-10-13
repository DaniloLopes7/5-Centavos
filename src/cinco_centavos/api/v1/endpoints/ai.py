"""Endpoints de Inteligência Artificial (RF17)."""

from decimal import Decimal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from cinco_centavos.ai import FinancialAdvisor
from cinco_centavos.api.v1.deps import get_current_user
from cinco_centavos.core.database import get_db
from cinco_centavos.models import User
from cinco_centavos.repositories import CategoryRepository, TransactionRepository
from cinco_centavos.schemas import (
    AnomalyList,
    CashFlowPrediction,
    CategoryPrediction,
    InsightsResponse,
    TrainStatus,
    TransactionPredictInput,
)
from cinco_centavos.schemas.ai import Anomaly

router = APIRouter(prefix="/ai", tags=["IA"], dependencies=[Depends(get_current_user)])


def _trained_advisor(db: Session, user: User):
    """Treina um FinancialAdvisor com os dados do usuário autenticado."""
    transactions = TransactionRepository(db).list_by_user(user.id)
    advisor = FinancialAdvisor()
    df, count = advisor.train(transactions)
    return advisor, df, count


@router.post("/train", response_model=TrainStatus, summary="Treinar modelos com seus dados")
def train(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> TrainStatus:
    _, _, count = _trained_advisor(db, current_user)
    return TrainStatus(
        status="ok",
        message="Modelos avaliados com os dados do usuário autenticado",
        transactions_used=count,
    )


@router.post(
    "/predict-category",
    response_model=CategoryPrediction,
    summary="Predizer categoria pela descrição",
)
def predict_category(
    data: TransactionPredictInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CategoryPrediction:
    advisor, _, _ = _trained_advisor(db, current_user)
    name, confidence = advisor.classifier.predict(data.description)

    category_id = None
    for category in CategoryRepository(db).list_by_user(current_user.id):
        if category.name == name:
            category_id = category.id
            break

    return CategoryPrediction(
        category_id=category_id, category_name=name, confidence=confidence
    )


@router.get("/insights", response_model=InsightsResponse, summary="Insights personalizados")
def insights(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> InsightsResponse:
    advisor, df, _ = _trained_advisor(db, current_user)

    anomalies = advisor.detector.detect(df)
    expected_receitas, expected_despesas, basis = advisor.predictor.predict(df)
    prediction = CashFlowPrediction(
        period_months=3,
        expected_receitas=expected_receitas,
        expected_despesas=expected_despesas,
        projected_balance=expected_receitas - expected_despesas,
        basis=basis,
    )
    return InsightsResponse(
        insights=advisor.generate_insights(df),
        profile=advisor.clusterer.profile(df),
        cashflow_prediction=prediction,
        anomalies_detected=len(anomalies),
    )


@router.get(
    "/cashflow-prediction",
    response_model=CashFlowPrediction,
    summary="Previsão de fluxo de caixa",
)
def cashflow_prediction(
    period_months: int = Query(default=3, ge=1, le=12),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CashFlowPrediction:
    advisor, df, _ = _trained_advisor(db, current_user)
    expected_receitas, expected_despesas, basis = advisor.predictor.predict(
        df, period_months
    )
    return CashFlowPrediction(
        period_months=period_months,
        expected_receitas=expected_receitas,
        expected_despesas=expected_despesas,
        projected_balance=expected_receitas - expected_despesas,
        basis=basis,
    )


@router.get("/anomalies", response_model=AnomalyList, summary="Gastos anômalos detectados")
def anomalies(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> AnomalyList:
    advisor, df, _ = _trained_advisor(db, current_user)
    detected = advisor.detector.detect(df)
    items = [
        Anomaly(
            transaction_id=int(row.id),
            description=str(row.description),
            amount=Decimal(str(round(float(row.amount), 2))),
            date=row.date.strftime("%Y-%m-%d"),
            reason=str(getattr(row, "reason", "Padrão atípico")),
        )
        for row in detected.itertuples()
    ]
    return AnomalyList(total=len(items), anomalies=items)
