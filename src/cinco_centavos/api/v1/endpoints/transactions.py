"""Endpoints de transações financeiras (RF04, RF05, RF08, RF09)."""

from datetime import date

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from cinco_centavos.api.v1.deps import get_current_user
from cinco_centavos.core.database import get_db
from cinco_centavos.models import TransactionType, User
from cinco_centavos.schemas import (
    TransactionCreate,
    TransactionResponse,
    TransactionUpdate,
)
from cinco_centavos.services import TransactionService

router = APIRouter(
    prefix="/transactions", tags=["Transações"], dependencies=[Depends(get_current_user)]
)


@router.get("", response_model=list[TransactionResponse], summary="Listar transações")
def list_transactions(
    account_id: int | None = Query(default=None),
    type: TransactionType | None = Query(default=None),
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return TransactionService(db).list_transactions(
        current_user.id,
        account_id=account_id,
        type=type,
        start_date=start_date,
        end_date=end_date,
    )


@router.post(
    "",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar receita/despesa",
)
def create_transaction(
    data: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return TransactionService(db).create_transaction(current_user.id, data)


@router.get("/{transaction_id}", response_model=TransactionResponse, summary="Obter transação")
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return TransactionService(db).get_transaction(current_user.id, transaction_id)


@router.put(
    "/{transaction_id}", response_model=TransactionResponse, summary="Atualizar transação"
)
def update_transaction(
    transaction_id: int,
    data: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return TransactionService(db).update_transaction(current_user.id, transaction_id, data)


@router.delete(
    "/{transaction_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover transação",
)
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    TransactionService(db).delete_transaction(current_user.id, transaction_id)
