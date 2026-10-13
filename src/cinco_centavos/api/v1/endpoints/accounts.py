"""Endpoints de contas financeiras (RF03, RF07)."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from cinco_centavos.api.v1.deps import get_current_user
from cinco_centavos.core.database import get_db
from cinco_centavos.models import User
from cinco_centavos.schemas import (
    AccountCreate,
    AccountResponse,
    AccountUpdate,
    AccountWithBalance,
)
from cinco_centavos.services import AccountService

router = APIRouter(
    prefix="/users/me/accounts", tags=["Contas"], dependencies=[Depends(get_current_user)]
)


@router.get("", response_model=list[AccountWithBalance], summary="Listar contas com saldo")
def list_accounts(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> list[AccountWithBalance]:
    return AccountService(db).list_accounts(current_user.id)


@router.post(
    "",
    response_model=AccountResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar conta",
)
def create_account(
    data: AccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return AccountService(db).create_account(current_user.id, data)


@router.get("/{account_id}", response_model=AccountWithBalance, summary="Obter conta")
def get_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AccountWithBalance:
    return AccountService(db).get_account(current_user.id, account_id)


@router.put("/{account_id}", response_model=AccountResponse, summary="Atualizar conta")
def update_account(
    account_id: int,
    data: AccountUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return AccountService(db).update_account(current_user.id, account_id, data)


@router.delete(
    "/{account_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Remover conta"
)
def delete_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    AccountService(db).delete_account(current_user.id, account_id)
