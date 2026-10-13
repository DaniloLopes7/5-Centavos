"""Utilitários de segurança: hash de senhas (bcrypt) e tokens JWT."""

from datetime import UTC, datetime, timedelta

import bcrypt
from jose import JWTError, jwt

from cinco_centavos.core.config import settings


def hash_password(password: str) -> str:
    """Gera o hash bcrypt de uma senha em texto puro."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    """Verifica se uma senha em texto puro corresponde ao hash armazenado."""
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except ValueError:
        return False


def create_access_token(subject: str | int, expires_delta: timedelta | None = None) -> str:
    """Cria um JWT assinado contendo o identificador do usuário no claim ``sub``."""
    expire = datetime.now(UTC) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    payload = {"sub": str(subject), "exp": expire}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> str | None:
    """Decodifica um JWT e retorna o ``sub``; retorna ``None`` se inválido/expirado."""
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.jwt_algorithm]
        )
        subject: str | None = payload.get("sub")
        return subject
    except JWTError:
        return None
