"""Repositório de metas financeiras (isoladas por usuário)."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from cinco_centavos.models import Goal
from cinco_centavos.repositories.base import BaseRepository


class GoalRepository(BaseRepository[Goal]):
    """Todas as consultas filtram por ``user_id`` (privacidade/isolamento)."""

    def __init__(self, db: Session) -> None:
        super().__init__(db, Goal)

    def list_by_user(self, user_id: int) -> list[Goal]:
        """Lista metas pertencentes a um usuário."""
        stmt = select(Goal).where(Goal.user_id == user_id).order_by(Goal.id)
        return list(self.db.scalars(stmt))

    def get_owned(self, goal_id: int, user_id: int) -> Goal | None:
        """Busca uma meta apenas se pertencer ao usuário informado."""
        stmt = select(Goal).where(Goal.id == goal_id, Goal.user_id == user_id)
        return self.db.scalars(stmt).first()
