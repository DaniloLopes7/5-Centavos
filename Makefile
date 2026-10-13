.PHONY: help install test test-unit test-integration run-api run-dashboard run-etl docker-build docker-up docker-down docker-logs lint clean

PYTHON := .venv/bin/python
PIP := .venv/bin/pip

help: ## Mostra os comandos disponíveis
	@grep -E '^[a-zA-Z_-]+:.*?## ' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

install: ## Cria o venv e instala as dependências
	python3 -m venv .venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

test: ## Executa toda a suíte de testes
	PYTHONPATH=src $(PYTHON) -m pytest tests/ -v

test-unit: ## Apenas testes unitários
	PYTHONPATH=src $(PYTHON) -m pytest tests/unit -v

test-integration: ## Testes de integração e e2e
	PYTHONPATH=src $(PYTHON) -m pytest tests/integration tests/e2e -v

run-api: ## Inicia a API REST em modo reload (http://localhost:8000/docs)
	PYTHONPATH=src $(PYTHON) -m uvicorn cinco_centavos.api.main:app --host 0.0.0.0 --port 8000 --reload

run-dashboard: ## Inicia o dashboard Streamlit (http://localhost:8501)
	PYTHONPATH=src $(PYTHON) -m streamlit run src/cinco_centavos/dashboard/app.py --server.port 8501

run-etl: ## Carrega os dados seed de data/ no banco
	PYTHONPATH=src $(PYTHON) -m cinco_centavos.etl.load_data

docker-build: ## Constrói a imagem Docker
	docker compose build

docker-up: ## Sobe PostgreSQL + API + Dashboard
	docker compose up -d

docker-etl: ## Executa o ETL dentro dos containers
	docker compose --profile etl run --rm etl

docker-down: ## Para e remove containers
	docker compose down

docker-logs: ## Logs dos serviços
	docker compose logs -f

lint: ## Checagem de sintaxe/estilo básica
	$(PYTHON) -m compileall -q src tests

clean: ## Remove caches e artefatos
	find . -type d -name __pycache__ -not -path "./.venv/*" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .mypy_cache
