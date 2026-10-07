from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime
from decimal import Decimal

from src.schemas import TransactionCreate, TransactionUpdate, TransactionResponse
from src.services import TransactionService, AccountService, CategoryService
from src.api.v1.deps import get_current_user

router = APIRouter(prefix="/transactions", tags=["Transações"])


@router.get("", response_model=List[TransactionResponse])
async def list_transactions(
    account_id: int = None,
    current_user: dict = Depends(get_current_user)
):
    """Lista transações do usuário, opcionalmente filtradas por conta."""
    if account_id:
        account = AccountService.get_account(account_id)
        if not account or account.get("user_id") != current_user["id"]:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conta não encontrada.")
        transactions = TransactionService.get_account_transactions(account_id)
    else:
        transactions = TransactionService.get_user_transactions(current_user["id"])
    
    return [TransactionResponse.model_validate(t) for t in transactions]


@router.post("", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(transaction_data: TransactionCreate, current_user: dict = Depends(get_current_user)):
    """Cria uma nova transação."""
    # Verifica se a conta pertence ao usuário
    account = AccountService.get_account(transaction_data.account_id)
    if not account or account.get("user_id") != current_user["id"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conta não encontrada.")
    
    # Verifica se a categoria pertence ao usuário
    category = CategoryService.get_category(transaction_data.category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada.")
    
    try:
        success = TransactionService.create(
            transaction_data.account_id,
            transaction_data.category_id,
            transaction_data.description,
            transaction_data.amount,
            transaction_data.type.value,
            transaction_data.date
        )
        if not success:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao criar transação.")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    # Retorna a transação criada
    transactions = TransactionService.get_account_transactions(transaction_data.account_id)
    if transactions:
        return TransactionResponse.model_validate(transactions[0])
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao recuperar transação criada.")


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(transaction_id: int, current_user: dict = Depends(get_current_user)):
    """Obtém uma transação específica."""
    transaction = TransactionService.get_transaction(transaction_id)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transação não encontrada.")
    
    # Verifica se a transação pertence ao usuário (através da conta)
    account = AccountService.get_account(transaction["account_id"])
    if not account or account.get("user_id") != current_user["id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado.")
    
    return TransactionResponse.model_validate(transaction)


@router.put("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: int,
    transaction_data: TransactionUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Atualiza uma transação."""
    transaction = TransactionService.get_transaction(transaction_id)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transação não encontrada.")
    
    # Verifica se a transação pertence ao usuário
    account = AccountService.get_account(transaction["account_id"])
    if not account or account.get("user_id") != current_user["id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado.")
    
    update_data = transaction_data.model_dump(exclude_unset=True)
    if "type" in update_data:
        update_data["type"] = update_data["type"].value
    
    if update_data:
        try:
            success = TransactionService.update(transaction_id, **update_data)
            if not success:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao atualizar transação.")
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    updated_transaction = TransactionService.get_transaction(transaction_id)
    return TransactionResponse.model_validate(updated_transaction)


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(transaction_id: int, current_user: dict = Depends(get_current_user)):
    """Remove uma transação."""
    transaction = TransactionService.get_transaction(transaction_id)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transação não encontrada.")
    
    # Verifica se a transação pertence ao usuário
    account = AccountService.get_account(transaction["account_id"])
    if not account or account.get("user_id") != current_user["id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado.")
    
    success = TransactionService.delete(transaction_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao remover transação.")