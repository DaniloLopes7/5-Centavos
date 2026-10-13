"""Schemas de autenticação."""

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRegister(BaseModel):
    """Payload de registro de usuário (CU01)."""

    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class UserLogin(BaseModel):
    """Payload de login (CU02)."""

    email: EmailStr
    password: str


class Token(BaseModel):
    """Token de acesso JWT retornado no login."""

    model_config = ConfigDict(from_attributes=True)

    access_token: str
    token_type: str = "bearer"
