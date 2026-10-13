"""Repositório de transações (isolamento via conta do usuário)."""

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from cinco_centavos.models import Account, Transaction, TransactionType
from cinco_centavos.repositories.base import BaseRepository


class TransactionRepository(BaseRepository[Transaction]):
    """Transações pertencem a contas, que pertencem ao usuário."""

    def __init__(self, db: Session) -> None:
        super().__init__(db, Transaction)

    def _user_filter(self, user_id: int) :
        """Condição compartilhada: transação pertence ao usuário."""
        return Transaction.account.has(Account.user_id == user_id)

    def list_by_user(
        self,
        user_id: int,
        *,
        account_id: int | None = None,
        type: TransactionType | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[Transaction]:
        """Lista transações do usuário com filtros opcionais de período/conta/tipo."""
        conditions = [self._user_filter(user_id)]
        if account_id is not None:
            conditions.append(Transaction.account_id == account_id)
        if type is not None:
            conditions.append(Transaction.type == type)
        if start_date is not None:
            conditions.append(Transaction.date >= start_date)
        if end_date is not None:
            conditions.append(Transaction.date <= end_date)

        stmt = (
            select(Transaction)
            .where(*conditions)
            .order_by(Transaction.date.desc(), Transaction.id.desc())
        )
        return list(self.db.scalars(stmt))

    def get_owned(self, transaction_id: int, user_id: int) -> Transaction | None:
        """Busca uma transação apenas se pertencer ao usuário informado."""
        stmt = select(Transaction).where(
            Transaction.id == transaction_id, self._user_filter(user_id)
        )
        return self.db.scalars(stmt).first()
