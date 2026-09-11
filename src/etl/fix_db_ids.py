import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "data", "finance.db")

def fix_users_table():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        print("Iniciando correção da tabela de usuários...")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR NOT NULL,
                email VARCHAR NOT NULL UNIQUE,
                password_hash VARCHAR NOT NULL,
                created_at DATETIME NOT NULL
            )
        """)

        cursor.execute("SELECT name, email, password_hash, created_at FROM users")
        rows = cursor.fetchall()

        for row in rows:
            cursor.execute(
                "INSERT INTO users_new (name, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
                row
            )

        cursor.execute("DROP TABLE users")
        cursor.execute("ALTER TABLE users_new RENAME TO users")

        conn.commit()
        print(f"Sucesso: {len(rows)} usuários corrigidos e IDs restaurados.")
        conn.close()
    except Exception as e:
        print(f"Erro ao corrigir banco: {e}")

if __name__ == "__main__":
    fix_users_table()
