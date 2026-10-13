"""Serviço de usuários: registro, autenticação e categorias padrão."""

from sqlalchemy.orm import Session

from cinco_centavos.core.security import hash_password, verify_password
from cinco_centavos.models import CategoryType, User
from cinco_centavos.repositories import CategoryRepository, UserRepository
from cinco_centavos.schemas.auth import UserRegister
from cinco_centavos.services.exceptions import ConflictError, UnauthorizedError

DEFAULT_CATEGORIES: list[tuple[str, CategoryType]] = [
    ("Salário", CategoryType.RECEITA),
    ("Freelance", CategoryType.RECEITA),
    ("Investimentos", CategoryType.RECEITA),
    ("Outras Receitas", CategoryType.RECEITA),
    ("Alimentação", CategoryType.DESPESA),
    ("Transporte", CategoryType.DESPESA),
    ("Moradia", CategoryType.DESPESA),
    ("Saúde", CategoryType.DESPESA),
    ("Lazer", CategoryType.DESPESA),
    ("Educação", CategoryType.DESPESA),
]


class UserService:
    """Regras de negócio de usuários (RF01, RF02)."""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.users = UserRepository(db)
        self.categories = CategoryRepository(db)

    def register(self, data: UserRegister) -> User:
        """Cadastra um usuário e cria suas categorias padrão (CU01)."""
        if self.users.get_by_email(data.email) is not None:
            raise ConflictError("E-mail já cadastrado")

        user = self.users.create(
            name=data.name,
            email=data.email,
            password_hash=hash_password(data.password),
        )
        self._create_default_categories(user.id)
        self.db.commit()
        return user

    def authenticate(self, email: str, password: str) -> User:
        """Valida credenciais de login (CU02)."""
        user = self.users.get_by_email(email)
        if user is None or not verify_password(password, user.password_hash):
            raise UnauthorizedError("Credenciais inválidas")
        return user

    def _create_default_categories(self, user_id: int) -> None:
        for name, type_ in DEFAULT_CATEGORIES:
            if not self.categories.exists_named(user_id, name, type_):
                self.categories.create(user_id=user_id, name=name, type=type_)
