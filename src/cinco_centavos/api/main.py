"""Ponto de entrada da API REST do 5 Centavos (FastAPI)."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from cinco_centavos import __version__
from cinco_centavos.api.limiter import limiter
from cinco_centavos.api.v1.router import api_router
from cinco_centavos.core.config import settings
from cinco_centavos.core.database import init_db
from cinco_centavos.core.logging import configure_logging, get_logger
from cinco_centavos.services.exceptions import (
    BusinessRuleError,
    ConflictError,
    DomainError,
    NotFoundError,
    UnauthorizedError,
)

configure_logging()
logger = get_logger(__name__)

_EXCEPTION_STATUS = {
    NotFoundError: 404,
    ConflictError: 409,
    BusinessRuleError: 422,
    UnauthorizedError: 401,
}


def _register_exception_handlers(app: FastAPI) -> None:
    """Mapeia exceções de domínio para respostas HTTP padronizadas."""
    for exception_class, status_code in _EXCEPTION_STATUS.items():

        async def handler(
            request: Request,
            exc: DomainError,
            _status: int = status_code,
        ) -> JSONResponse:
            return JSONResponse(status_code=_status, content={"detail": str(exc)})

        app.add_exception_handler(exception_class, handler)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Startup: cria tabelas e executa o ETL opcionalmente."""
    logger.info("api.starting", env=settings.app_env, version=__version__)
    init_db()
    if settings.run_etl:
        from cinco_centavos.etl.load_data import run as run_etl

        run_etl()
    yield
    logger.info("api.stopping")


app = FastAPI(
    title=settings.app_name,
    version=__version__,
    description=(
        "Plataforma de gestão financeira pessoal com Analytics e IA. "
        "Autenticação via Bearer Token (POST /api/v1/auth/login)."
    ),
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
_register_exception_handlers(app)


@app.get("/health", tags=["Infra"], summary="Health check")
def health() -> dict[str, str]:
    return {"status": "ok", "version": __version__}


@app.get("/", tags=["Infra"], summary="Redirecionamento lógico")
def root() -> dict[str, str]:
    return {
        "message": f"{settings.app_name} API",
        "docs": "/docs",
        "health": "/health",
    }
