from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel

from src.api.v1.deps import get_current_user
from src.ai import advisor, TransactionClassifier, AnomalyDetector, CashFlowPredictor

router = APIRouter(prefix="/ai", tags=["Inteligência Artificial"])


class TrainRequest(BaseModel):
    force: bool = False


class PredictionRequest(BaseModel):
    description: str


class PredictionResponse(BaseModel):
    category: str


class InsightsResponse(BaseModel):
    insights: List[dict]
    predictions: List[dict]
    anomalies: List[dict]


@router.post("/train", response_model=dict)
async def train_models(
    request: TrainRequest,
    current_user: dict = Depends(get_current_user)
):
    """Treina todos os modelos de IA com os dados do usuário."""
    results = advisor.train_all(current_user["id"])
    return {
        "status": "success",
        "message": "Treinamento concluído.",
        "results": results
    }


@router.post("/predict-category", response_model=PredictionResponse)
async def predict_category(
    request: PredictionRequest,
    current_user: dict = Depends(get_current_user)
):
    """Prediz a categoria de uma transação baseada na descrição."""
    category = advisor.classifier.predict(request.description)
    return PredictionResponse(category=category)


@router.get("/insights", response_model=InsightsResponse)
async def get_insights(current_user: dict = Depends(get_current_user)):
    """Retorna insights financeiros personalizados, previsões e anomalias."""
    insights_data = advisor.get_insights(current_user["id"])
    return InsightsResponse(**insights_data)


@router.get("/cashflow-prediction")
async def get_cashflow_prediction(
    months: int = 3,
    current_user: dict = Depends(get_current_user)
):
    """Retorna previsão de fluxo de caixa para os próximos meses."""
    if not advisor.cashflow_predictor.is_trained:
        # Tentar treinar
        advisor.cashflow_predictor.train(
            advisor.anomaly_detector._prepare_data.__self__ if hasattr(advisor.anomaly_detector, '_prepare_data') else []
        )
    
    predictions = advisor.cashflow_predictor.predict_next_months(months)
    return {
        "predictions": predictions,
        "months": months
    }


@router.get("/anomalies")
async def get_anomalies(
    limit: int = 10,
    current_user: dict = Depends(get_current_user)
):
    """Retorna transações anômalas detectadas."""
    insights_data = advisor.get_insights(current_user["id"])
    return {
        "anomalies": insights_data.get("anomalies", [])[:limit],
        "total": len(insights_data.get("anomalies", []))
    }


@router.get("/spending-profile")
async def get_spending_profile(current_user: dict = Depends(get_current_user)):
    """Retorna o perfil de gasto do usuário baseado em clustering."""
    # Este endpoint precisaria de dados de múltiplos usuários para funcionar
    # Por enquanto, retorna um placeholder
    return {
        "profile": "Equilibrado",
        "description": "Gastos bem distribuídos entre essenciais e lazer",
        "recommendations": [
            "Revise assinaturas mensais",
            "Automatize investimentos",
            "Mantenha reserva de emergência"
        ]
    }