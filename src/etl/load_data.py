import pandas as pd
from sqlalchemy import create_engine, text
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "finance.db")

def get_engine():
    return create_engine(f"sqlite:///{DB_PATH}")

def load_csv_to_sql(engine, filename, table_name):
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

        # Reset e criação de tabelas
        tables_schema = {
            "users": """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR NOT NULL,
                    email VARCHAR NOT NULL UNIQUE,
                    password_hash VARCHAR NOT NULL,
                    created_at DATETIME NOT NULL
                )
            """,
            "accounts": """
                CREATE TABLE IF NOT EXISTS accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    name VARCHAR NOT NULL,
                    type VARCHAR NOT NULL,
                    initial_balance DECIMAL NOT NULL,
                    created_at DATETIME NOT NULL
                )
            """,
            "categories": """
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    name VARCHAR NOT NULL,
                    type VARCHAR NOT NULL
                )
            """,
            "goals": """
                CREATE TABLE IF NOT EXISTS goals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    name VARCHAR NOT NULL,
                    target_amount DECIMAL NOT NULL,
                    current_amount DECIMAL NOT NULL,
                    deadline DATE,
                    created_at DATETIME NOT NULL
                )
            """,
            "transactions": """
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_id INTEGER NOT NULL,
                    category_id INTEGER NOT NULL,
                    description VARCHAR NOT NULL,
                    amount DECIMAL NOT NULL,
                    type VARCHAR NOT NULL,
                    date DATE NOT NULL,
                    created_at DATETIME NOT NULL,
                    FOREIGN KEY(account_id) REFERENCES accounts(id),
                    FOREIGN KEY(category_id) REFERENCES categories(id)
                )
            """
        }

        # Drop tabelas para aplicar novo schema
        for table in ["transactions", "goals", "categories", "accounts", "users"]:
            conn.execute(text(f"DROP TABLE IF EXISTS {table}"))

        # Criação de tabelas
        for table in ["users", "accounts", "categories", "goals", "transactions"]:
            conn.execute(text(tables_schema[table]))

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
