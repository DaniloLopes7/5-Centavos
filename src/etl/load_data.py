import pandas as pd
from sqlalchemy import create_engine, text
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "finance.db")

def get_engine():
    """Cria a conexão com o banco de dados SQLite."""
    return create_engine(f"sqlite:///{DB_PATH}")

def load_csv_to_sql(engine, filename, table_name):
    """Lê um CSV e carrega no banco de dados."""
    path = os.path.join(DATA_DIR, filename)
    print(f"Carregando {filename} para a tabela {table_name}...")

    df = pd.read_csv(path)
    df = df.drop_duplicates(subset=['id'])

    df.to_sql(table_name, engine, if_exists='append', index=False)
    print(f"Sucesso: {len(df)} registros inseridos em {table_name}.")

def run_etl():
    engine = get_engine()

    with engine.connect() as conn:
        conn.execute(text("PRAGMA foreign_keys = OFF;"))

        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
        existing_tables = [row[0] for row in result]

        tables_to_clean = ["transactions", "goals", "categories", "accounts", "users"]
        for table in tables_to_clean:
            if table in existing_tables:
                conn.execute(text(f"DELETE FROM {table};"))

        conn.execute(text("PRAGMA foreign_keys = ON;"))
        conn.commit()

    load_order = [
        ("usuarios.csv", "users"),
        ("contas.csv", "accounts"),
        ("categorias.csv", "categories"),
        ("metas.csv", "goals"),
        ("transacoes.csv", "transactions"),
    ]

    for csv_file, table in load_order:
        load_csv_to_sql(engine, csv_file, table)

    print("\n--- ETL Concluído com Sucesso! ---")
    print(f"Banco de dados atualizado em: {DB_PATH}")

if __name__ == "__main__":
    run_etl()
