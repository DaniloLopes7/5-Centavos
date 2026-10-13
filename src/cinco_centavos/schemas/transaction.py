"""Schemas de transações financeiras."""

import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from cinco_centavos.models.enums import TransactionType


class TransactionCreate(BaseModel):
    """Payload de criação de transação (CU04/CU05)."""

    account_id: int
    category_id: int
    description: str = Field(min_length=1, max_length=255)
    amount: Decimal = Field(gt=0)  # regra de negócio: valor obrigatoriamente positivo
    type: TransactionType
    date: datetime.date


class TransactionUpdate(BaseModel):
    """Payload de atualização de transação (CU08)."""

    account_id: int | None = None
    category_id: int | None = None
    description: str | None = Field(default=None, min_length=1, max_length=255)
    amount: Decimal | None = Field(default=None, gt=0)
    type: TransactionType | None = None
    date: datetime.date | None = None


class TransactionResponse(BaseModel):
    """Representação de uma transação."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    account_id: int
    category_id: int
    description: str
    amount: Decimal
    type: TransactionType
    date: datetime.date
