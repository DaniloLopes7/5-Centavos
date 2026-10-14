"""Configurações da aplicação carregadas de variáveis de ambiente (.env)."""

from functools import lru_cache

from pydantic import AliasChoices, Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações centralizadas do sistema 5 Centavos."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # SQLite local; integrações Postgres podem injetar qualquer um destes nomes.
    database_url: str = Field(
        default="sqlite:///./data/five_centavos.db",
        validation_alias=AliasChoices(
            "DATABASE_URL",
            "POSTGRES_URL",
            "POSTGRES_PRISMA_URL",
            "NEON_DATABASE_URL",
            # URLs sem pool ficam como fallback; em serverless prefira uma URL pooled.
            "DATABASE_URL_UNPOOLED",
            "POSTGRES_URL_NON_POOLING",
        ),
    )

    # Segurança / JWT
    secret_key: str = "chave-insegura-de-desenvolvimento"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # Aplicação
    app_name: str = "5 Centavos"
    app_env: str = "development"
    log_level: str = "INFO"
    cors_origins: str = (
        "https://5-centavos.vercel.app,http://localhost:8501,"
        "http://localhost:3000,http://localhost:8080"
    )

    # ETL
    run_etl: bool = False

    @field_validator("database_url")
    @classmethod
    def normalize_postgres_url(cls, value: str) -> str:
        """Normaliza esquemas PostgreSQL para o driver síncrono instalado."""
        if value.startswith("postgres://"):
            return "postgresql+psycopg2://" + value.removeprefix("postgres://")
        if value.startswith("postgresql://"):
            return "postgresql+psycopg2://" + value.removeprefix("postgresql://")
        if value.startswith("postgresql+psycopg://"):
            return "postgresql+psycopg2://" + value.removeprefix(
                "postgresql+psycopg://"
            )
        return value

    @model_validator(mode="after")
    def require_secret_key_in_production(self) -> "Settings":
        """Recusa segredos ausentes ou de exemplo no ambiente de produção."""
        invalid_secret_values = {
            "chave-insegura-de-desenvolvimento",
            "troque-esta-chave-por-uma-chave-segura-aleatoria",
        }
        if self.is_production and (
            len(self.secret_key.strip()) < 32
            or self.secret_key.strip() in invalid_secret_values
        ):
            raise ValueError(
                "SECRET_KEY deve ser definida em produção com pelo menos 32 caracteres; "
                "não use o valor de desenvolvimento do .env.example."
            )
        return self

    @property
    def cors_origin_list(self) -> list[str]:
        """Retorna as origens CORS como lista."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def is_production(self) -> bool:
        """Indica se a aplicação está em ambiente de produção."""
        return self.app_env.lower() == "production"


@lru_cache
def get_settings() -> Settings:
    """Retorna a instância única (cacheada) das configurações."""
    return Settings()


settings = get_settings()
