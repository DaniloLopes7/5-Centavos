import unittest
import sqlite3
from sqlalchemy import create_engine, text
from src.cinco_centavos import database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.test_engine = create_engine("sqlite:///:memory:")

        schema = [
            "CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR NOT NULL, email VARCHAR NOT NULL UNIQUE, password_hash VARCHAR NOT NULL, created_at DATETIME NOT NULL)",
            "CREATE TABLE accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, name VARCHAR NOT NULL, type VARCHAR NOT NULL, initial_balance DECIMAL NOT NULL, created_at DATETIME NOT NULL)",
            "CREATE TABLE categories (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, name VARCHAR NOT NULL, type VARCHAR NOT NULL)",
            "CREATE TABLE goals (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, name VARCHAR NOT NULL, target_amount DECIMAL NOT NULL, current_amount DECIMAL NOT NULL, deadline DATE, created_at DATETIME NOT NULL)",
            "CREATE TABLE transactions (id INTEGER PRIMARY KEY AUTOINCREMENT, account_id INTEGER NOT NULL, category_id INTEGER NOT NULL, description VARCHAR NOT NULL, amount DECIMAL NOT NULL, type VARCHAR NOT NULL, date DATE NOT NULL, created_at DATETIME NOT NULL, FOREIGN KEY(account_id) REFERENCES accounts(id), FOREIGN KEY(category_id) REFERENCES categories(id))"
        ]

        with self.test_engine.begin() as conn:
            for statement in schema:
                conn.execute(text(statement))

        self.original_engine = database.engine
        database.engine = self.test_engine

    def tearDown(self):
        database.engine = self.original_engine

    def test_password_security(self):
        password = "secure_password123"
        hashed = database.hash_password(password)
        self.assertNotEqual(hashed, password)
        self.assertTrue(database.check_password(password, hashed))
        self.assertFalse(database.check_password("wrong_password", hashed))

    def test_user_lifecycle(self):
        name, email, password = "Test User", "test@example.com", "password123"
        self.assertTrue(database.create_user(name, email, password))

        user = database.get_user_by_email(email)
        self.assertIsNotNone(user)
        self.assertEqual(user['name'], name)
        self.assertFalse(database.create_user("Other", email, "pass"))

        user_by_id = database.get_user_by_id(user['id'])
        self.assertEqual(user_by_id['email'], email)

    def test_account_management(self):
        database.create_user("User", "acc@example.com", "pass")
        user = database.get_user_by_email("acc@example.com")
        self.assertTrue(database.create_account(user['id'], "NuConta", "Corrente", 1000.00))
        accounts = database.get_accounts_by_user(user['id'])
        self.assertEqual(len(accounts), 1)
        self.assertEqual(accounts[0]['name'], "NuConta")

    def test_category_management(self):
        database.create_user("User", "cat@example.com", "pass")
        user = database.get_user_by_email("cat@example.com")
        self.assertTrue(database.create_category(user['id'], "Lazer", "DESPESA"))
        categories = database.get_categories_by_user(user['id'])
        self.assertEqual(len(categories), 1)
        self.assertEqual(categories[0]['name'], "Lazer")

    def test_transaction_and_balance(self):
        database.create_user("User", "fin@example.com", "pass")
        user = database.get_user_by_email("fin@example.com")
        uid = user['id']

        database.create_account(uid, "Carteira", "Espécie", 100.00)
        aid = database.get_accounts_by_user(uid)[0]['id']

        database.create_category(uid, "Lazer", "DESPESA")
        cid = database.get_categories_by_user(uid)[0]['id']
        self.assertTrue(database.add_transaction(aid, cid, "Cinema", 50.00, "DESPESA", "2023-10-01"))

        database.create_category(uid, "Salário", "RECEITA")
        cid_rev = database.get_categories_by_user(uid)[1]['id']
        self.assertTrue(database.add_transaction(aid, cid_rev, "Pagamento", 200.00, "RECEITA", "2023-10-02"))

        self.assertEqual(database.calculate_balance(aid), 250.00)

    def test_goal_management(self):
        database.create_user("User", "goal@example.com", "pass")
        user = database.get_user_by_email("goal@example.com")
        uid = user['id']
        self.assertTrue(database.create_goal(uid, "Viagem", 5000.00, "2024-12-31"))
        goal = database.get_goals_by_user(uid)[0]
        self.assertTrue(database.update_goal_progress(goal['id'], 1000.00))
        updated_goal = database.get_goals_by_user(uid)[0]
        self.assertEqual(float(updated_goal['current_amount']), 1000.00)

if __name__ == "__main__":
    unittest.main()
