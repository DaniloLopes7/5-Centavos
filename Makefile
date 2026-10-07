# Makefile para 5 Centavos
# Comandos úteis para desenvolvimento

.PHONY: help install test run-api run-dashboard run-etl docker-build docker-up docker-down docker-logs clean

# Variáveis
PYTHON := python3
VENV := .venv
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest
UVICORN := $(VENV)/bin/uvicorn
STREAMLIT := $(VENV)/bin/streamlit

# Ajuda
help:
	@echo "5 Centavos - Comandos disponíveis:"
	@echo ""
	@echo "Desenvolvimento:"
	@echo "  install       - Instala dependências no ambiente virtual"
	@echo "  test          - Executa testes"
	@echo "  run-api       - Inicia API FastAPI (porta 8000)"
	@echo "  run-dashboard - Inicia Dashboard Streamlit (porta 8501)"
	@echo "  run-etl       - Executa processo ETL"
	@echo "  run-cli       - Inicia interface de linha de comando"
	@echo ""
	@echo "Docker:"
	@echo "  docker-build  - Constrói imagens Docker"
	@echo "  docker-up     - Inicia todos os containers"
	@echo "  docker-down   - Para todos os containers"
	@echo "  docker-logs   - Mostra logs dos containers"
	@echo "  docker-etl    - Executa ETL via Docker"
	@echo ""
	@echo "Utilitários:"
	@echo "  clean         - Remove arquivos temporários"
	@echo "  lint          - Executa linting (se configurado)"
	@echo "  format        - Formata código (se configurado)"

# Instalar dependências
install:
	@echo "Criando ambiente virtual..."
	@python3 -m venv $(VENV)
	@echo "Instalando dependências..."
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements.txt
	@echo "Ambiente pronto! Use 'source $(VENV)/bin/activate' para ativar."

# Testes
test:
	@$(PYTEST) tests/ -v

# API
run-api:
	@$(UVICORN) src.api.main:app --host 0.0.0.0 --port 8000 --reload

# Dashboard
run-dashboard:
	@$(STREAMLIT) run src/dashboard/app.py --server.port 8501 --server.address 0.0.0.0

# ETL
run-etl:
	@$(PYTHON) src/etl/load_data.py

# CLI
run-cli:
	@$(PYTHON) -m src.cinco_centavos.main

# Docker
docker-build:
	@docker-compose build

docker-up:
	@docker-compose up -d

docker-down:
	@docker-compose down

docker-logs:
	@docker-compose logs -f

docker-etl:
	@docker-compose --profile etl run --rm etl

# Limpeza
clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf .coverage htmlcov 2>/dev/null || true
	@echo "Limpeza concluída."

# Linting (opcional - requer flake8/black)
lint:
	@$(VENV)/bin/flake8 src/ || echo "flake8 não instalado"
	@$(VENV)/bin/black --check src/ || echo "black não instalado"

format:
	@$(VENV)/bin/black src/ || echo "black não instalado"
	@$(VENV)/bin/isort src/ || echo "isort não instalado"

# Banco de dados
db-reset:
	@$(PYTHON) src/etl/load_data.py

db-shell:
	@psql postgresql://user:user@localhost:5432/five_centavos