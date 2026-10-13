"""Schemas Pydantic v2 para validação e serialização."""

from cinco_centavos.schemas.account import (
    AccountCreate,
    AccountResponse,
    AccountUpdate,
    AccountWithBalance,
)
from cinco_centavos.schemas.ai import (
    AnomalyList,
    CategoryPrediction,
    CashFlowPrediction,
    InsightsResponse,
    TransactionPredictInput,
    TrainStatus,
)
from cinco_centavos.schemas.analytics import (
    CategoryBreakdownItem,
    FinancialSummary,
    MonthlyEvolutionItem,
)
from cinco_centavos.schemas.auth import Token, UserLogin, UserRegister
from cinco_centavos.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from cinco_centavos.schemas.goal import (
    GoalCreate,
    GoalProgressRequest,
    GoalResponse,
    GoalUpdate,
)
from cinco_centavos.schemas.transaction import (
    TransactionCreate,
    TransactionResponse,
    TransactionUpdate,
)
from cinco_centavos.schemas.user import UserResponse

__all__ = [
    "AccountCreate",
    "AccountResponse",
    "AccountUpdate",
    "AccountWithBalance",
    "AnomalyList",
    "CashFlowPrediction",
    "CategoryBreakdownItem",
    "CategoryCreate",
    "CategoryPrediction",
    "CategoryResponse",
    "CategoryUpdate",
    "FinancialSummary",
    "GoalCreate",
    "GoalProgressRequest",
    "GoalResponse",
    "GoalUpdate",
    "InsightsResponse",
    "MonthlyEvolutionItem",
    "Token",
    "TrainStatus",
    "TransactionCreate",
    "TransactionPredictInput",
    "TransactionResponse",
    "TransactionUpdate",
    "UserLogin",
    "UserRegister",
    "UserResponse",
]
