"""Endpoints de categorias financeiras (RF06)."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from cinco_centavos.api.v1.deps import get_current_user
from cinco_centavos.core.database import get_db
from cinco_centavos.models import CategoryType, User
from cinco_centavos.schemas import CategoryCreate, CategoryResponse, CategoryUpdate
from cinco_centavos.services import CategoryService

router = APIRouter(
    prefix="/users/me/categories",
    tags=["Categorias"],
    dependencies=[Depends(get_current_user)],
)


@router.get("", response_model=list[CategoryResponse], summary="Listar categorias")
def list_categories(
    type: CategoryType | None = Query(default=None, description="Filtra por tipo"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return CategoryService(db).list_categories(current_user.id, type)


@router.post(
    "",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar categoria",
)
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return CategoryService(db).create_category(current_user.id, data)


@router.put(
    "/{category_id}", response_model=CategoryResponse, summary="Atualizar categoria"
)
def update_category(
    category_id: int,
    data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return CategoryService(db).update_category(current_user.id, category_id, data)


@router.delete(
    "/{category_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Remover categoria"
)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    CategoryService(db).delete_category(current_user.id, category_id)
