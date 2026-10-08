# Dockerfile para 5 Centavos
FROM python:3.12-slim

WORKDIR /app

# Instalar dependências do sistema (inclui postgresql-client para pg_isready)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libpq5 \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências Python globalmente
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Copiar entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Criar usuário não-root e ajustar permissões
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Expor portas
EXPOSE 8000 8501

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    API_BASE_URL=http://api:8000/api/v1 \
    RUN_ETL=false

# Entrypoint que aguarda PostgreSQL e roda ETL opcional
ENTRYPOINT ["/entrypoint.sh"]

# Comando padrão (API)
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
