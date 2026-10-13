"""Repositório base genérico com operações CRUD comuns."""

from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

ModelT = TypeVar("ModelT")


class BaseRepository(Generic[ModelT]):
    """CRUD genérico sobre uma sessão SQLAlchemy."""

    def __init__(self, db: Session, model: type[ModelT]) -> None:
        self.db = db
        self.model = model

    def get(self, obj_id: int) -> ModelT | None:
        """Busca um registro pelo identificador."""
        return self.db.get(self.model, obj_id)

    def create(self, **fields: object) -> ModelT:
        """Cria e persiste um novo registro."""
        obj = self.model(**fields)
        self.db.add(obj)
        self.db.flush()
        self.db.refresh(obj)
        return obj

    def update(self, obj: ModelT, fields: dict) -> ModelT:
        """Aplica alterações a um registro existente."""
        for key, value in fields.items():
            setattr(obj, key, value)
        self.db.flush()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: ModelT) -> None:
        """Remove um registro."""
        self.db.delete(obj)
        self.db.flush()

    def list_all(self) -> list[ModelT]:
        """Lista todos os registros do modelo."""
        return list(self.db.scalars(select(self.model)))
