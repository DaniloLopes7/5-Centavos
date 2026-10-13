"""Schemas de metas financeiras."""

import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class GoalCreate(BaseModel):
    """Payload de criação de meta (CU12)."""

    name: str = Field(min_length=1, max_length=120)
    target_amount: Decimal = Field(gt=0)
    deadline: datetime.date | None = None


class GoalUpdate(BaseModel):
    """Payload de atualização de meta."""

    name: str | None = Field(default=None, min_length=1, max_length=120)
    target_amount: Decimal | None = Field(default=None, gt=0)
    deadline: datetime.date | None = None


class GoalProgressRequest(BaseModel):
    """Payload para adicionar progresso (economia) a uma meta."""

    amount: Decimal = Field(gt=0)


class GoalResponse(BaseModel):
    """Representação de uma meta com progresso percentual calculado."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    target_amount: Decimal
    current_amount: Decimal
    deadline: datetime.date | None

    @property
    def progress_pct(self) -> float:
        """Percentual de conclusão da meta (0 a 100)."""
        if self.target_amount <= 0:
            return 0.0
        return round(float(self.current_amount / self.target_amount) * 100, 2)
