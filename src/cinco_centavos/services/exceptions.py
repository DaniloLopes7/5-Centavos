"""Exceções de domínio usadas pela camada de serviços."""


class DomainError(Exception):
    """Erro de regra de negócio genérico."""


class NotFoundError(DomainError):
    """Registro não encontrado (ou não pertence ao usuário)."""


class ConflictError(DomainError):
    """Conflito de unicidade (ex.: e-mail já cadastrado)."""


class BusinessRuleError(DomainError):
    """Violação de regra de negócio (ex.: valor inválido, tipo incompatível)."""


class UnauthorizedError(DomainError):
    """Credenciais inválidas ou token ausente/expirado."""
