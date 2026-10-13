"""Fixtures compartilhadas da suíte de testes.

Cada teste recebe um banco SQLite em memória isolado
(criado a partir dos modelos ORM) e um TestClient da API.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from cinco_centavos.api.limiter import limiter
from cinco_centavos.api.main import app
from cinco_centavos.core.database import Base, get_db

# O TestClient faz chamadas sempre do mesmo endereço; desligamos o rate
# limiting para que a suíte não falhe por 429 acumulados entre testes.
limiter.enabled = False


@pytest.fixture
def db_session():
    """Sessão SQLAlchemy sobre SQLite em memória, com todas as tabelas."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    testing_session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    session: Session = testing_session()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)
        engine.dispose()


@pytest.fixture
def client(db_session):
    """TestClient da API com a dependência de banco sobreposta."""

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    try:
        # Sem `with`: a fixture de sessão já cria as tabelas e o lifespan
        # (init_db no banco real) não precisa ser executado.
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


@pytest.fixture
def auth_headers(client):
    """Registra um usuário padrão e retorna headers autenticados."""
    client.post(
        "/api/v1/auth/register",
        json={"name": "Usuário Teste", "email": "teste@example.com", "password": "senha123"},
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "teste@example.com", "password": "senha123"},
    )
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


@pytest.fixture
def account_id(client, auth_headers):
    """Cria uma conta corrente com saldo inicial de R$ 1.000."""
    response = client.post(
        "/api/v1/users/me/accounts",
        json={"name": "Conta Corrente", "type": "CORRENTE", "initial_balance": "1000.00"},
        headers=auth_headers,
    )
    return response.json()["id"]


@pytest.fixture
def category_ids(client, auth_headers):
    """IDs de uma categoria de receita e uma de despesa do usuário padrão."""
    categories = client.get("/api/v1/users/me/categories", headers=auth_headers).json()
    receita = next(c["id"] for c in categories if c["type"] == "RECEITA")
    despesa = next(c["id"] for c in categories if c["type"] == "DESPESA")
    return {"receita": receita, "despesa": despesa}
