"""Schemas de contas financeiras."""

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from cinco_centavos.models.enums import AccountType


class AccountCreate(BaseModel):
    """Payload de criação de conta (CU03)."""

    name: str = Field(min_length=1, max_length=120)
    type: AccountType
    initial_balance: Decimal = Decimal("0")


class AccountUpdate(BaseModel):
    """Payload de atualização de conta."""

    name: str | None = Field(default=None, min_length=1, max_length=120)
    type: AccountType | None = None
    initial_balance: Decimal | None = None


class AccountResponse(BaseModel):
    """Representação de uma conta financeira."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    type: AccountType
    initial_balance: Decimal


class AccountWithBalance(AccountResponse):
    """Conta com o saldo calculado (inicial + receitas − despesas)."""

    balance: Decimal
