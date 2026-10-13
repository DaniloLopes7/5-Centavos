"""Endpoints de metas financeiras (RF16)."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from cinco_centavos.api.v1.deps import get_current_user
from cinco_centavos.core.database import get_db
from cinco_centavos.models import User
from cinco_centavos.schemas import (
    GoalCreate,
    GoalProgressRequest,
    GoalResponse,
    GoalUpdate,
)
from cinco_centavos.services import GoalService

router = APIRouter(
    prefix="/goals", tags=["Metas"], dependencies=[Depends(get_current_user)]
)


@router.get("", response_model=list[GoalResponse], summary="Listar metas")
def list_goals(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return GoalService(db).list_goals(current_user.id)


@router.post(
    "",
    response_model=GoalResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar meta",
)
def create_goal(
    data: GoalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return GoalService(db).create_goal(current_user.id, data)


@router.get("/{goal_id}", response_model=GoalResponse, summary="Obter meta")
def get_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return GoalService(db).get_goal(current_user.id, goal_id)


@router.put("/{goal_id}", response_model=GoalResponse, summary="Atualizar meta")
def update_goal(
    goal_id: int,
    data: GoalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return GoalService(db).update_goal(current_user.id, goal_id, data)


@router.post(
    "/{goal_id}/progress", response_model=GoalResponse, summary="Adicionar progresso"
)
def add_progress(
    goal_id: int,
    data: GoalProgressRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return GoalService(db).add_progress(current_user.id, goal_id, data.amount)


@router.delete(
    "/{goal_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Remover meta"
)
def delete_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    GoalService(db).delete_goal(current_user.id, goal_id)
