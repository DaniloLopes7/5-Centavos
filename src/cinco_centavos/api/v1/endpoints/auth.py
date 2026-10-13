"""Endpoints de autenticação (RF01, RF02)."""

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from cinco_centavos.api.limiter import limiter
from cinco_centavos.api.v1.deps import get_current_user
from cinco_centavos.core.database import get_db
from cinco_centavos.core.security import create_access_token
from cinco_centavos.models import User
from cinco_centavos.schemas import Token, UserLogin, UserRegister, UserResponse
from cinco_centavos.services import UserService

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar novo usuário",
)
@limiter.limit("5/minute")
def register(request: Request, data: UserRegister, db: Session = Depends(get_db)) -> User:
    return UserService(db).register(data)


@router.post("/login", response_model=Token, summary="Login com JWT")
@limiter.limit("10/minute")
def login(request: Request, data: UserLogin, db: Session = Depends(get_db)) -> Token:
    user = UserService(db).authenticate(email=data.email, password=data.password)
    return Token(access_token=create_access_token(user.id))


@router.get("/me", response_model=UserResponse, summary="Usuário autenticado")
def me(current_user: User = Depends(get_current_user)) -> User:
    return current_user
