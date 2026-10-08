#!/bin/bash
set -e

echo "[Entrypoint] Iniciando 5 Centavos..."

# Aguardar PostgreSQL ficar disponível
echo "[Entrypoint] Aguardando PostgreSQL..."
until pg_isready -h postgres -U user -d five_centavos > /dev/null 2>&1; do
    sleep 2
done
echo "[Entrypoint] PostgreSQL pronto!"

# Executar ETL se solicitado (para inicializar banco)
if [ "$RUN_ETL" = "true" ]; then
    echo "[Entrypoint] Executando ETL..."
    python3 src/etl/load_data.py
    echo "[Entrypoint] ETL concluído!"
fi

# Executar comando passado
exec "$@"