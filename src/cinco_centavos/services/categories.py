"""Serviço de categorias financeiras."""

from sqlalchemy.orm import Session

from cinco_centavos.models import Category, CategoryType
from cinco_centavos.repositories import CategoryRepository
from cinco_centavos.schemas.category import CategoryCreate, CategoryUpdate
from cinco_centavos.services.exceptions import ConflictError, NotFoundError


class CategoryService:
    """Regras de negócio de categorias (RF06, CU10)."""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.categories = CategoryRepository(db)

    def list_categories(
        self, user_id: int, type: CategoryType | None = None
    ) -> list[Category]:
        return self.categories.list_by_user(user_id, type)

    def create_category(self, user_id: int, data: CategoryCreate) -> Category:
        if self.categories.exists_named(user_id, data.name, data.type):
            raise ConflictError(
                f"Categoria '{data.name}' ({data.type}) já existe para este usuário"
            )
        category = self.categories.create(user_id=user_id, name=data.name, type=data.type)
        self.db.commit()
        return category

    def update_category(
        self, user_id: int, category_id: int, data: CategoryUpdate
    ) -> Category:
        category = self._get_owned(user_id, category_id)
        fields = data.model_dump(exclude_unset=True)
        name = fields.get("name", category.name)
        type_ = fields.get("type", category.type)
        if self.categories.exists_named(user_id, name, type_):
            raise ConflictError(
                f"Categoria '{name}' ({type_}) já existe para este usuário"
            )
        category = self.categories.update(category, fields)
        self.db.commit()
        return category

    def delete_category(self, user_id: int, category_id: int) -> None:
        category = self._get_owned(user_id, category_id)
        self.categories.delete(category)
        self.db.commit()

    def _get_owned(self, user_id: int, category_id: int) -> Category:
        category = self.categories.get_owned(category_id, user_id)
        if category is None:
            raise NotFoundError("Categoria não encontrada")
        return category
