"""Schemas de categorias financeiras."""

from pydantic import BaseModel, ConfigDict, Field

from cinco_centavos.models.enums import CategoryType


class CategoryCreate(BaseModel):
    """Payload de criação de categoria (CU10)."""

    name: str = Field(min_length=1, max_length=120)
    type: CategoryType


class CategoryUpdate(BaseModel):
    """Payload de atualização de categoria."""

    name: str | None = Field(default=None, min_length=1, max_length=120)
    type: CategoryType | None = None


class CategoryResponse(BaseModel):
    """Representação de uma categoria."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    type: CategoryType
