"""Serviço de contas financeiras."""

from decimal import Decimal

from sqlalchemy.orm import Session

from cinco_centavos.models import Account
from cinco_centavos.repositories import AccountRepository, AnalyticsRepository
from cinco_centavos.schemas.account import AccountCreate, AccountUpdate, AccountWithBalance
from cinco_centavos.services.exceptions import NotFoundError


class AccountService:
    """Regras de negócio de contas (RF03, RF07)."""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.accounts = AccountRepository(db)
        self.analytics = AnalyticsRepository(db)

    def list_accounts(self, user_id: int) -> list[AccountWithBalance]:
        """Lista contas do usuário com saldo atual calculado (CU06)."""
        accounts = self.accounts.list_by_user(user_id)
        nets = self.analytics.account_transaction_totals(user_id)
        return [self._with_balance(account, nets.get(account.id, Decimal(0))) for account in accounts]

    def get_account(self, user_id: int, account_id: int) -> AccountWithBalance:
        """Obtém uma conta do usuário com saldo."""
        account = self._get_owned(user_id, account_id)
        nets = self.analytics.account_transaction_totals(user_id)
        return self._with_balance(account, nets.get(account.id, Decimal(0)))

    @staticmethod
    def _with_balance(account: Account, net: Decimal) -> AccountWithBalance:
        """Monta o DTO da conta com saldo = inicial + receitas − despesas."""
        return AccountWithBalance(
            id=account.id,
            name=account.name,
            type=account.type,
            initial_balance=account.initial_balance,
            balance=account.initial_balance + net,
        )

    def create_account(self, user_id: int, data: AccountCreate) -> Account:
        """Cria uma conta vinculada ao usuário (CU03)."""
        account = self.accounts.create(
            user_id=user_id,
            name=data.name,
            type=data.type,
            initial_balance=data.initial_balance,
        )
        self.db.commit()
        return account

    def update_account(self, user_id: int, account_id: int, data: AccountUpdate) -> Account:
        """Atualiza dados de uma conta do usuário."""
        account = self._get_owned(user_id, account_id)
        fields = data.model_dump(exclude_unset=True)
        account = self.accounts.update(account, fields)
        self.db.commit()
        return account

    def delete_account(self, user_id: int, account_id: int) -> None:
        """Remove uma conta e suas transações (cascade no banco)."""
        account = self._get_owned(user_id, account_id)
        self.accounts.delete(account)
        self.db.commit()

    def _get_owned(self, user_id: int, account_id: int) -> Account:
        account = self.accounts.get_owned(account_id, user_id)
        if account is None:
            raise NotFoundError("Conta não encontrada")
        return account
