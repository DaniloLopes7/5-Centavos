from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from decimal import Decimal

from src.schemas import GoalCreate, GoalUpdate, GoalResponse, GoalProgressUpdate
from src.services import GoalService
from src.api.v1.deps import get_current_user

router = APIRouter(prefix="/goals", tags=["Metas"])


@router.get("", response_model=List[GoalResponse])
async def list_goals(current_user: dict = Depends(get_current_user)):
    """Lista todas as metas do usuário."""
    goals = GoalService.get_user_goals(current_user["id"])
    return [GoalResponse.model_validate(g) for g in goals]


@router.post("", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
async def create_goal(goal_data: GoalCreate, current_user: dict = Depends(get_current_user)):
    """Cria uma nova meta."""
    success = GoalService.create(
        current_user["id"],
        goal_data.name,
        goal_data.target_amount,
        goal_data.deadline
    )
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao criar meta.")
    
    goals = GoalService.get_user_goals(current_user["id"])
    if goals:
        return GoalResponse.model_validate(goals[-1])
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao recuperar meta criada.")


@router.get("/{goal_id}", response_model=GoalResponse)
async def get_goal(goal_id: int, current_user: dict = Depends(get_current_user)):
    """Obtém uma meta específica."""
    goal = GoalService.get_goal(goal_id)
    if not goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meta não encontrada.")
    
    # Verifica se a meta pertence ao usuário
    # As metas já são filtradas por user_id no service
    return GoalResponse.model_validate(goal)


@router.put("/{goal_id}", response_model=GoalResponse)
async def update_goal(
    goal_id: int,
    goal_data: GoalUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Atualiza uma meta."""
    goal = GoalService.get_goal(goal_id)
    if not goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meta não encontrada.")
    
    update_data = goal_data.model_dump(exclude_unset=True)
    if update_data:
        success = GoalService.update(goal_id, **update_data)
        if not success:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao atualizar meta.")
    
    updated_goal = GoalService.get_goal(goal_id)
    return GoalResponse.model_validate(updated_goal)


@router.post("/{goal_id}/progress", response_model=GoalResponse)
async def add_goal_progress(
    goal_id: int,
    progress_data: GoalProgressUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Adiciona progresso a uma meta."""
    goal = GoalService.get_goal(goal_id)
    if not goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meta não encontrada.")
    
    success = GoalService.update_progress(goal_id, progress_data.amount)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao atualizar progresso da meta.")
    
    updated_goal = GoalService.get_goal(goal_id)
    return GoalResponse.model_validate(updated_goal)


@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_goal(goal_id: int, current_user: dict = Depends(get_current_user)):
    """Remove uma meta."""
    goal = GoalService.get_goal(goal_id)
    if not goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meta não encontrada.")
    
    success = GoalService.delete(goal_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao remover meta.")