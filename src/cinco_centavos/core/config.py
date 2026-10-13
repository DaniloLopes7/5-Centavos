"""Configurações da aplicação carregadas de variáveis de ambiente (.env)."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações centralizadas do sistema 5 Centavos."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Banco de dados (desenvolvimento local usa SQLite; Docker sobrescreve via env)
    database_url: str = "sqlite:///./data/five_centavos.db"

    # Segurança / JWT
    secret_key: str = "chave-insegura-de-desenvolvimento"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # Aplicação
    app_name: str = "5 Centavos"
    app_env: str = "development"
    log_level: str = "INFO"
    cors_origins: str = (
        "http://localhost:8501,http://localhost:3000,"
        "http://localhost:8080,http://127.0.0.1:8080"
    )

    # ETL
    run_etl: bool = False

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
