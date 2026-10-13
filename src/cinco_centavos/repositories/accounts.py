"""Repositório de contas financeiras (isoladas por usuário)."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from cinco_centavos.models import Account
from cinco_centavos.repositories.base import BaseRepository


class AccountRepository(BaseRepository[Account]):
    """Todas as consultas filtram por ``user_id`` (privacidade/isolamento)."""

    def __init__(self, db: Session) -> None:
        super().__init__(db, Account)

    def list_by_user(self, user_id: int) -> list[Account]:
        """Lista as contas pertencentes a um usuário."""
        stmt = select(Account).where(Account.user_id == user_id).order_by(Account.id)
        return list(self.db.scalars(stmt))

    def get_owned(self, account_id: int, user_id: int) -> Account | None:
        """Busca uma conta apenas se pertencer ao usuário informado."""
        stmt = select(Account).where(Account.id == account_id, Account.user_id == user_id)
        return self.db.scalars(stmt).first()
