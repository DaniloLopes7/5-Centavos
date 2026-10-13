"""Repositório de usuários."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from cinco_centavos.models import User
from cinco_centavos.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Acesso a dados de usuários."""

    def __init__(self, db: Session) -> None:
        super().__init__(db, User)

    def get_by_email(self, email: str) -> User | None:
        """Busca usuário pelo e-mail (único por regra de negócio)."""
        return self.db.scalars(select(User).where(User.email == email)).first()
