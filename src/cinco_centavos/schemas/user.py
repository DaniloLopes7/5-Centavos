"""Schemas de usuário."""

from pydantic import BaseModel, ConfigDict, EmailStr


class UserResponse(BaseModel):
    """Representação pública de um usuário (nunca expõe senha/hash)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
