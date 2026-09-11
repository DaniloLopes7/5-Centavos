import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "data", "finance.db")

def fix_all_tables():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        print("Iniciando reconstrução total do banco de dados...")

        cursor.execute("PRAGMA foreign_keys = OFF;")

        cursor.execute("CREATE TABLE users_new (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR NOT NULL, email VARCHAR NOT NULL UNIQUE, password_hash VARCHAR NOT NULL, created_at DATETIME NOT NULL)")
        cursor.execute("SELECT name, email, password_hash, created_at FROM users")
        for row in cursor.fetchall():
            cursor.execute("INSERT INTO users_new (name, email, password_hash, created_at) VALUES (?, ?, ?, ?)", row)
        cursor.execute("DROP TABLE users")
        cursor.execute("ALTER TABLE users_new RENAME TO users")

        cursor.execute("CREATE TABLE accounts_new (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, name VARCHAR NOT NULL, type VARCHAR NOT NULL, initial_balance DECIMAL NOT NULL, created_at DATETIME NOT NULL)")
        cursor.execute("SELECT user_id, name, type, initial_balance, created_at FROM accounts")
        for row in cursor.fetchall():
            cursor.execute("INSERT INTO accounts_new (user_id, name, type, initial_balance, created_at) VALUES (?, ?, ?, ?, ?)", row)
        cursor.execute("DROP TABLE accounts")
        cursor.execute("ALTER TABLE accounts_new RENAME TO accounts")

        cursor.execute("CREATE TABLE categories_new (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, name VARCHAR NOT NULL, type VARCHAR NOT NULL)")
        cursor.execute("SELECT user_id, name, type FROM categories")
        for row in cursor.fetchall():
            cursor.execute("INSERT INTO categories_new (user_id, name, type) VALUES (?, ?, ?)", row)
        cursor.execute("DROP TABLE categories")
        cursor.execute("ALTER TABLE categories_new RENAME TO categories")

        cursor.execute("CREATE TABLE goals_new (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, name VARCHAR NOT NULL, target_amount DECIMAL NOT NULL, current_amount DECIMAL NOT NULL, deadline DATE, created_at DATETIME NOT NULL)")
        cursor.execute("SELECT user_id, name, target_amount, current_amount, deadline, created_at FROM goals")
        for row in cursor.fetchall():
            cursor.execute("INSERT INTO goals_new (user_id, name, target_amount, current_amount, deadline, created_at) VALUES (?, ?, ?, ?, ?, ?)", row)
        cursor.execute("DROP TABLE goals")
        cursor.execute("ALTER TABLE goals_new RENAME TO goals")

        cursor.execute("DROP TABLE IF EXISTS transactions")
        cursor.execute("""
            CREATE TABLE transactions (
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
        """)

        conn.commit()
        cursor.execute("PRAGMA foreign_keys = ON;")
        conn.close()
        print("\n✅ Banco de dados reconstruído com sucesso!")
        print("Agora todos os IDs são gerados automaticamente (AUTOINCREMENT).")
    except Exception as e:
        print(f"Erro crítico ao reconstruir banco: {e}")

if __name__ == "__main__":
    fix_all_tables()
