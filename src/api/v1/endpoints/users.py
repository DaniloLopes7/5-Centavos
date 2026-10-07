from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from src.schemas import UserResponse, AccountResponse, CategoryResponse, TransactionResponse, GoalResponse
from src.schemas import AccountCreate, AccountUpdate, CategoryCreate, CategoryUpdate
from src.schemas import TransactionCreate, TransactionUpdate, GoalCreate, GoalUpdate, GoalProgressUpdate
from src.schemas import FinancialSummary, CategorySummary, MonthlySummary
from src.services import AccountService, CategoryService, TransactionService, GoalService, AnalyticsService
from src.api.v1.deps import get_current_user

router = APIRouter(prefix="/users", tags=["Usuários"])


# Account endpoints
@router.get("/me/accounts", response_model=List[AccountResponse])
async def list_accounts(current_user: dict = Depends(get_current_user)):
    """Lista todas as contas do usuário."""
    accounts = AccountService.get_user_accounts(current_user["id"])
    return [AccountResponse.model_validate(acc) for acc in accounts]


@router.post("/me/accounts", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
async def create_account(account_data: AccountCreate, current_user: dict = Depends(get_current_user)):
    """Cria uma nova conta."""
    success = AccountService.create(
        current_user["id"],
        account_data.name,
        account_data.type,
        account_data.initial_balance
    )
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao criar conta.")
    
    # Retorna a conta criada (busca a última criada)
    accounts = AccountService.get_user_accounts(current_user["id"])
    if accounts:
        return AccountResponse.model_validate(accounts[-1])
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao recuperar conta criada.")


@router.get("/me/accounts/{account_id}", response_model=AccountResponse)
async def get_account(account_id: int, current_user: dict = Depends(get_current_user)):
    """Obtém uma conta específica."""
    account = AccountService.get_account(account_id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conta não encontrada.")
    
    # Verifica se a conta pertence ao usuário
    if account.get("user_id") != current_user["id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado.")
    
    return AccountResponse.model_validate(account)


@router.put("/me/accounts/{account_id}", response_model=AccountResponse)
async def update_account(
    account_id: int,
    account_data: AccountUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Atualiza uma conta."""
    account = AccountService.get_account(account_id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conta não encontrada.")
    
    if account.get("user_id") != current_user["id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado.")
    
    update_data = account_data.model_dump(exclude_unset=True)
    if update_data:
        success = AccountService.update(account_id, **update_data)
        if not success:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao atualizar conta.")
    
    updated_account = AccountService.get_account(account_id)
    return AccountResponse.model_validate(updated_account)


@router.delete("/me/accounts/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(account_id: int, current_user: dict = Depends(get_current_user)):
    """Remove uma conta."""
    account = AccountService.get_account(account_id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conta não encontrada.")
    
    if account.get("user_id") != current_user["id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado.")
    
    success = AccountService.delete(account_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao remover conta.")


# Category endpoints
@router.get("/me/categories", response_model=List[CategoryResponse])
async def list_categories(current_user: dict = Depends(get_current_user)):
    """Lista todas as categorias do usuário."""
    categories = CategoryService.get_user_categories(current_user["id"])
    return [CategoryResponse.model_validate(cat) for cat in categories]


@router.post("/me/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(category_data: CategoryCreate, current_user: dict = Depends(get_current_user)):
    """Cria uma nova categoria."""
    success = CategoryService.create(
        current_user["id"],
        category_data.name,
        category_data.type.value
    )
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao criar categoria.")
    
    categories = CategoryService.get_user_categories(current_user["id"])
    if categories:
        return CategoryResponse.model_validate(categories[-1])
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao recuperar categoria criada.")


@router.get("/me/categories/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int, current_user: dict = Depends(get_current_user)):
    """Obtém uma categoria específica."""
    category = CategoryService.get_category(category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada.")
    return CategoryResponse.model_validate(category)


@router.put("/me/categories/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Atualiza uma categoria."""
    category = CategoryService.get_category(category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada.")
    
    # Verifica se a categoria pertence ao usuário (opcional, já que as categorias são por usuário)
    update_data = category_data.model_dump(exclude_unset=True)
    if "type" in update_data:
        update_data["type"] = update_data["type"].value
    
    if update_data:
        success = CategoryService.update(category_id, **update_data)
        if not success:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao atualizar categoria.")
    
    updated_category = CategoryService.get_category(category_id)
    return CategoryResponse.model_validate(updated_category)


@router.delete("/me/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int, current_user: dict = Depends(get_current_user)):
    """Remove uma categoria."""
    category = CategoryService.get_category(category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria não encontrada.")
    
    success = CategoryService.delete(category_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao remover categoria.")