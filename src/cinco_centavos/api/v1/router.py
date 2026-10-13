"""Agregador dos routers da API v1."""

from fastapi import APIRouter

from cinco_centavos.api.v1.endpoints import (
    accounts,
    ai,
    analytics,
    auth,
    categories,
    goals,
    transactions,
)

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth.router)
api_router.include_router(accounts.router)
api_router.include_router(categories.router)
api_router.include_router(transactions.router)
api_router.include_router(goals.router)
api_router.include_router(analytics.router)
api_router.include_router(ai.router)
