from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal
from enum import Enum


class TransactionType(str, Enum):
    RECEITA = "RECEITA"
    DESPESA = "DESPESA"


class CategoryType(str, Enum):
    RECEITA = "RECEITA"
    DESPESA = "DESPESA"


# User Schemas
class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=50)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# Account Schemas
class AccountBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    type: str = Field(..., min_length=2, max_length=30)
    initial_balance: Decimal = Field(..., ge=0)


class AccountCreate(AccountBase):
    pass


class AccountUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    type: Optional[str] = Field(None, min_length=2, max_length=30)
    initial_balance: Optional[Decimal] = Field(None, ge=0)


class AccountResponse(AccountBase):
    id: int
    user_id: int
    created_at: datetime
    current_balance: Optional[Decimal] = None

    class Config:
        from_attributes = True


# Category Schemas
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    type: CategoryType


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    type: Optional[CategoryType] = None


class CategoryResponse(CategoryBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


# Transaction Schemas
class TransactionBase(BaseModel):
    account_id: int
    category_id: int
    description: str = Field(..., min_length=1, max_length=200)
    amount: Decimal = Field(..., gt=0)
    type: TransactionType
    date: datetime


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    account_id: Optional[int] = None
    category_id: Optional[int] = None
    description: Optional[str] = Field(None, min_length=1, max_length=200)
    amount: Optional[Decimal] = Field(None, gt=0)
    type: Optional[TransactionType] = None
    date: Optional[datetime] = None


class TransactionResponse(TransactionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Goal Schemas
class GoalBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    target_amount: Decimal = Field(..., gt=0)
    deadline: Optional[datetime] = None


class GoalCreate(GoalBase):
    pass


class GoalUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    target_amount: Optional[Decimal] = Field(None, gt=0)
    current_amount: Optional[Decimal] = Field(None, ge=0)
    deadline: Optional[datetime] = None


class GoalProgressUpdate(BaseModel):
    amount: Decimal = Field(..., gt=0)


class GoalResponse(GoalBase):
    id: int
    user_id: int
    current_amount: Decimal
    created_at: datetime
    progress_percentage: Optional[float] = None

    class Config:
        from_attributes = True


# Report Schemas
class FinancialSummary(BaseModel):
    total_revenue: Decimal
    total_expense: Decimal
    balance: Decimal
    accounts_count: int
    transactions_count: int


class CategorySummary(BaseModel):
    category_id: int
    category_name: str
    category_type: str
    total_amount: Decimal
    transactions_count: int
    percentage: float


class MonthlySummary(BaseModel):
    month: str
    revenue: Decimal
    expense: Decimal
    balance: Decimal