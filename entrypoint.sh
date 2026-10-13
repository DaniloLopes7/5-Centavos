#!/usr/bin/env bash
# Entrypoint do container. Modos: api | dashboard | etl
set -euo pipefail

MODE="${1:-api}"

# Espera o PostgreSQL ficar pronto (quando DATABASE_URL aponta para ele).
if [[ "${DATABASE_URL:-}" == postgresql* ]]; then
  echo "Aguardando PostgreSQL..."
  python - <<'PY'
import os, time
from urllib.parse import urlparse
import psycopg2

url = urlparse(os.environ["DATABASE_URL"].replace("+psycopg2", ""))
for attempt in range(30):
    try:
        psycopg2.connect(
            host=url.hostname, port=url.port or 5432,
            user=url.username, password=url.password,
            dbname=url.path.lstrip("/"), connect_timeout=2,
        ).close()
        print("PostgreSQL disponível.")
        break
    except psycopg2.OperationalError:
        time.sleep(2)
else:
    raise SystemExit("PostgreSQL não respondeu a tempo.")
PY
fi

if [[ "${RUN_ETL:-false}" == "true" ]]; then
  echo "Executando ETL de dados iniciais..."
  python -m cinco_centavos.etl.load_data
fi

case "$MODE" in
  api)
    exec uvicorn cinco_centavos.api.main:app --host 0.0.0.0 --port "${API_PORT:-8000}"
    ;;
  dashboard)
    exec streamlit run src/cinco_centavos/dashboard/app.py \
      --server.port "${DASHBOARD_PORT:-8501}" --server.address 0.0.0.0
    ;;
  etl)
    exec python -m cinco_centavos.etl.load_data
    ;;
  *)
    exec "$@"
    ;;
esac
