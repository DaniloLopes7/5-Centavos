from fastapi import APIRouter

from src.api.v1.endpoints import auth, users, transactions, goals, analytics, ai

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(transactions.router)
api_router.include_router(goals.router)
api_router.include_router(analytics.router)
api_router.include_router(ai.router)