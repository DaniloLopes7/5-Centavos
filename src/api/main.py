from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.api.v1.router import api_router
from src.cinco_centavos.database import engine
from src.cinco_centavos import database as db_module


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("[API] Iniciando aplicação...")
    yield
    # Shutdown
    print("[API] Finalizando aplicação...")
    engine.dispose()


app = FastAPI(
    title="5 Centavos API",
    description="API para gerenciamento financeiro pessoal com Analytics e IA",
    version="0.5.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "message": "5 Centavos API",
        "version": "0.5.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}