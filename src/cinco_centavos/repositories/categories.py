"""Repositório de categorias (isoladas por usuário)."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from cinco_centavos.models import Category, CategoryType
from cinco_centavos.repositories.base import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    """Todas as consultas filtram por ``user_id`` (privacidade/isolamento)."""

    def __init__(self, db: Session) -> None:
        super().__init__(db, Category)

    def list_by_user(self, user_id: int, type: CategoryType | None = None) -> list[Category]:
        """Lista categorias de um usuário, opcionalmente por tipo."""
        stmt = select(Category).where(Category.user_id == user_id).order_by(Category.id)
        if type is not None:
            stmt = stmt.where(Category.type == type)
        return list(self.db.scalars(stmt))

    def get_owned(self, category_id: int, user_id: int) -> Category | None:
        """Busca uma categoria apenas se pertencer ao usuário informado."""
        stmt = select(Category).where(
            Category.id == category_id, Category.user_id == user_id
        )
        return self.db.scalars(stmt).first()

    def exists_named(self, user_id: int, name: str, type: CategoryType) -> bool:
        """Verifica se já existe categoria com mesmo nome e tipo para o usuário."""
        stmt = select(func.count(Category.id)).where(
            Category.user_id == user_id,
            Category.name == name,
            Category.type == type,
        )
        return bool(self.db.scalar(stmt))
