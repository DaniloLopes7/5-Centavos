"""Serviço de transações financeiras."""

from datetime import date

from sqlalchemy.orm import Session

from cinco_centavos.models import Transaction, TransactionType
from cinco_centavos.repositories import (
    AccountRepository,
    CategoryRepository,
    TransactionRepository,
)
from cinco_centavos.schemas.transaction import TransactionCreate, TransactionUpdate
from cinco_centavos.services.exceptions import BusinessRuleError, NotFoundError


class TransactionService:
    """Regras de negócio de transações (RF04, RF05, RF08, RF09)."""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.transactions = TransactionRepository(db)
        self.accounts = AccountRepository(db)
        self.categories = CategoryRepository(db)

    def list_transactions(
        self,
        user_id: int,
        *,
        account_id: int | None = None,
        type: TransactionType | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[Transaction]:
        """Histórico de transações do usuário (CU07)."""
        return self.transactions.list_by_user(
            user_id,
            account_id=account_id,
            type=type,
            start_date=start_date,
            end_date=end_date,
        )

    def get_transaction(self, user_id: int, transaction_id: int) -> Transaction:
        return self._get_owned(user_id, transaction_id)

    def create_transaction(self, user_id: int, data: TransactionCreate) -> Transaction:
        """Registra receita/despesa validando vínculos e compatibilidade (CU04/CU05)."""
        self._validate_links(user_id, data.account_id, data.category_id, data.type)
        transaction = self.transactions.create(**data.model_dump())
        self.db.commit()
        return transaction

    def update_transaction(
        self, user_id: int, transaction_id: int, data: TransactionUpdate
    ) -> Transaction:
        """Atualiza transação revalidando vínculos e tipos (CU08)."""
        transaction = self._get_owned(user_id, transaction_id)
        fields = data.model_dump(exclude_unset=True)

        account_id = fields.get("account_id", transaction.account_id)
        category_id = fields.get("category_id", transaction.category_id)
        type_ = fields.get("type", transaction.type)
        self._validate_links(user_id, account_id, category_id, type_)

        transaction = self.transactions.update(transaction, fields)
        self.db.commit()
        return transaction

    def delete_transaction(self, user_id: int, transaction_id: int) -> None:
        """Remove uma transação (CU09); o saldo é recalculado por consulta."""
        transaction = self._get_owned(user_id, transaction_id)
        self.transactions.delete(transaction)
        self.db.commit()

    def _validate_links(
        self, user_id: int, account_id: int, category_id: int, type: TransactionType
    ) -> None:
        if self.accounts.get_owned(account_id, user_id) is None:
            raise NotFoundError("Conta não encontrada")

        category = self.categories.get_owned(category_id, user_id)
        if category is None:
            raise NotFoundError("Categoria não encontrada")

        # Regra de negócio: tipo da categoria deve ser compatível com a transação.
        if category.type.value != type.value:
            raise BusinessRuleError(
                f"Categoria de {category.type.value} incompatível com "
                f"transação de {type.value}"
            )

    def _get_owned(self, user_id: int, transaction_id: int) -> Transaction:
        transaction = self.transactions.get_owned(transaction_id, user_id)
        if transaction is None:
            raise NotFoundError("Transação não encontrada")
        return transaction
