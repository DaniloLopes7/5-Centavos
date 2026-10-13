# syntax=docker/dockerfile:1

# ---------------------------------------------------------------------------
# Etapa 1 — builder: compila as dependências em um venv isolado
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

# ---------------------------------------------------------------------------
# Etapa 2 — runtime: imagem enxuta, usuário não-root
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONPATH=/app/src

RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY src ./src
COPY data ./data
COPY .streamlit ./.streamlit
COPY entrypoint.sh ./entrypoint.sh

RUN chmod +x entrypoint.sh && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000 8501

ENTRYPOINT ["./entrypoint.sh"]
CMD ["api"]
