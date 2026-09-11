import pandas as pd
from sqlalchemy import create_engine
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "data", "finance.db")

def verify():
    if not os.path.exists(DB_PATH):
        print(f"Erro: Banco de dados não encontrado em {DB_PATH}")
        return

    engine = create_engine(f"sqlite:///{DB_PATH}")
    tables = ["users", "accounts", "categories", "goals", "transactions"]

    for table in tables:
        print(f"\n--- Tabela: {table} ---")
        try:
            df = pd.read_sql(f"SELECT * FROM {table}", engine)
            if df.empty:
                print("Tabela vazia.")
            else:
                print(df.to_string(index=False))
        except Exception as e:
            print(f"Erro ao ler tabela {table}: {e}")

if __name__ == "__main__":
    verify()
