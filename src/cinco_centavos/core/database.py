"""Infraestrutura de persistência: engine, sessões e base ORM (SQLAlchemy 2.0)."""

from collections.abc import Iterator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from cinco_centavos.core.config import settings


class Base(DeclarativeBase):
    """Classe base declarativa de todos os modelos ORM."""


def build_engine(database_url: str) -> Engine:
    """Cria a engine SQLAlchemy respeitando particularidades do SQLite."""
    connect_args = (
        {"check_same_thread": False} if database_url.startswith("sqlite") else {}
    )
    return create_engine(database_url, pool_pre_ping=True, connect_args=connect_args)


engine = build_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db() -> Iterator[Session]:
    """Dependência FastAPI: fornece uma sessão e garante seu fechamento."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Cria todas as tabelas mapeadas (idempotente — seguro no startup)."""
    # Importa os modelos para registrá-los no metadata antes do create_all.
    from cinco_centavos import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
