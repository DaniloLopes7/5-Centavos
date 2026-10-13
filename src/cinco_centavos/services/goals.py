"""Serviço de metas financeiras."""

from decimal import Decimal

from sqlalchemy.orm import Session

from cinco_centavos.models import Goal
from cinco_centavos.repositories import GoalRepository
from cinco_centavos.schemas.goal import GoalCreate, GoalUpdate
from cinco_centavos.services.exceptions import NotFoundError


class GoalService:
    """Regras de negócio de metas (RF16, CU12)."""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.goals = GoalRepository(db)

    def list_goals(self, user_id: int) -> list[Goal]:
        return self.goals.list_by_user(user_id)

    def get_goal(self, user_id: int, goal_id: int) -> Goal:
        return self._get_owned(user_id, goal_id)

    def create_goal(self, user_id: int, data: GoalCreate) -> Goal:
        goal = self.goals.create(
            user_id=user_id,
            name=data.name,
            target_amount=data.target_amount,
            current_amount=Decimal("0"),
            deadline=data.deadline,
        )
        self.db.commit()
        return goal

    def update_goal(self, user_id: int, goal_id: int, data: GoalUpdate) -> Goal:
        goal = self._get_owned(user_id, goal_id)
        goal = self.goals.update(goal, data.model_dump(exclude_unset=True))
        self.db.commit()
        return goal

    def add_progress(self, user_id: int, goal_id: int, amount: Decimal) -> Goal:
        """Incrementa o valor acumulado de uma meta."""
        goal = self._get_owned(user_id, goal_id)
        goal = self.goals.update(goal, {"current_amount": goal.current_amount + amount})
        self.db.commit()
        return goal

    def delete_goal(self, user_id: int, goal_id: int) -> None:
        goal = self._get_owned(user_id, goal_id)
        self.goals.delete(goal)
        self.db.commit()

    def _get_owned(self, user_id: int, goal_id: int) -> Goal:
        goal = self.goals.get_owned(goal_id, user_id)
        if goal is None:
            raise NotFoundError("Meta não encontrada")
        return goal
