"""Configuração de logging estruturado com structlog."""

import logging

import structlog

from cinco_centavos.core.config import settings


def configure_logging() -> None:
    """Inicializa o logging padrão (logs JSON em produção, console em desenvolvimento)."""
    processors: list = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]
    if settings.is_production:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer(colors=True))

    logging.basicConfig(level=settings.log_level, format="%(message)s")
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.getLevelName(settings.log_level)
        ),
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.typing.FilteringBoundLogger:
    """Retorna um logger estruturado identificado por ``name``."""
    return structlog.get_logger(name)
