# Dockerfile para 5 Centavos
# Multi-stage build para otimizar tamanho da imagem

# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copiar dependências instaladas do builder
COPY --from=builder /root/.local /root/.local

# Adicionar ao PATH
ENV PATH=/root/.local/bin:$PATH

# Copiar código da aplicação
COPY . .

# Criar usuário não-root
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Expor portas
EXPOSE 8000 8501

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    API_BASE_URL=http://localhost:8000/api/v1

# Comando padrão (API)
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]