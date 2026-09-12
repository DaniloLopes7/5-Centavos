import os
import sys
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import bcrypt

# Configurações de Caminho
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "data", "finance.db")
engine = create_engine(f"sqlite:///{DB_PATH}")

def ensure_database_exists():
    if not os.path.exists(DB_PATH):
        print("\n[INIT] Banco de dados não encontrado. Inicializando...")
        _run_etl_process()
        return

    query = "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
    result = execute_query(query, fetch=True)
    if not result:
        print("\n[INIT] Banco de dados incompleto. Re-inicializando...")
        _run_etl_process()

def _run_etl_process():
    try:
        src_path = os.path.join(BASE_DIR, "src")
        if src_path not in sys.path:
            sys.path.append(src_path)

        from etl.load_data import run_etl
        run_etl()
    except Exception as e:
        print(f"\n[INIT ERROR] Falha ao inicializar o banco de dados: {e}")

def execute_query(query, params=None, fetch=False):

    try:
        with engine.begin() as conn:
            result = conn.execute(text(query), params or {})
            if fetch:
                return [dict(row) for row in result.mappings()]
            return True
    except SQLAlchemyError as e:
        print(f"\n[DB ERROR] Query: {query} | Params: {params} | Error: {e}")
        return None

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_user(name, email, password):
    if get_user_by_email(email):
        print("Erro: Este e-mail já está cadastrado.")
        return False

    hashed_pw = hash_password(password)
    query = "INSERT INTO users (name, email, password_hash, created_at) VALUES (:name, :email, :pw, datetime('now'))"
    return execute_query(query, {"name": name, "email": email, "pw": hashed_pw})

def get_user_by_id(user_id):
    query = "SELECT * FROM users WHERE id = :user_id"
    results = execute_query(query, {"user_id": int(user_id)}, fetch=True)
    return results[0] if results else None

def get_user_by_email(email):
    query = "SELECT * FROM users WHERE email = :email"
    results = execute_query(query, {"email": email}, fetch=True)
    return results[0] if results else None

def get_accounts_by_user(user_id):
    if user_id is None:
        return []
    query = "SELECT * FROM accounts WHERE user_id = :user_id"
    return execute_query(query, {"user_id": int(user_id)}, fetch=True) or []

def get_account_by_id(account_id):
    if account_id is None:
        return None
    query = "SELECT * FROM accounts WHERE id = :account_id"
    results = execute_query(query, {"account_id": int(account_id)}, fetch=True)
    return results[0] if results else None

def create_account(user_id, name, account_type, initial_balance):
    if user_id is None:
        print("Erro: ID do usuário é inválido.")
        return False
    query = "INSERT INTO accounts (user_id, name, type, initial_balance, created_at) VALUES (:uid, :name, :type, :bal, datetime('now'))"
    return execute_query(query, {"uid": int(user_id), "name": name, "type": account_type, "bal": initial_balance})

def calculate_balance(account_id):
    account = get_account_by_id(account_id)
    if not account: return 0.0
    initial_balance = float(account['initial_balance'])

    query_rev = "SELECT SUM(amount) as total FROM transactions WHERE account_id = :acc_id AND type = 'RECEITA'"
    res_rev = execute_query(query_rev, {"acc_id": int(account_id)}, fetch=True)
    revenues = float(res_rev[0]['total']) if res_rev and res_rev[0]['total'] else 0.0

    query_exp = "SELECT SUM(amount) as total FROM transactions WHERE account_id = :acc_id AND type = 'DESPESA'"
    res_exp = execute_query(query_exp, {"acc_id": int(account_id)}, fetch=True)
    expenses = float(res_exp[0]['total']) if res_exp and res_exp[0]['total'] else 0.0

    return initial_balance + revenues - expenses

def add_transaction(account_id, category_id, description, amount, trans_type, date):
    if account_id is None or category_id is None:
        print("Erro: ID da conta ou categoria é inválido.")
        return False
    query = """
        INSERT INTO transactions (account_id, category_id, description, amount, type, date, created_at)
        VALUES (:acc_id, :cat_id, :desc, :amt, :type, :date, datetime('now'))
    """
    params = {"acc_id": int(account_id), "cat_id": int(category_id), "desc": description, "amt": amount, "type": trans_type, "date": date}
    return execute_query(query, params)

def get_transactions_by_account(account_id):
    query = "SELECT * FROM transactions WHERE account_id = :acc_id ORDER BY date DESC"
    return execute_query(query, {"acc_id": int(account_id)}, fetch=True) or []

def get_categories_by_user(user_id):
    query = "SELECT * FROM categories WHERE user_id = :user_id"
    return execute_query(query, {"user_id": int(user_id)}, fetch=True) or []

def create_category(user_id, name, cat_type):
    query = "INSERT INTO categories (user_id, name, type) VALUES (:uid, :name, :type)"
    return execute_query(query, {"uid": int(user_id), "name": name, "type": cat_type})

def create_default_categories(user_id):
    defaults = [
        ("Alimentação", "DESPESA"),
        ("Lazer", "DESPESA"),
        ("Transporte", "DESPESA"),
        ("Saúde", "DESPESA"),
        ("Educação", "DESPESA"),
        ("Moradia", "DESPESA"),
        ("Salário", "RECEITA"),
        ("Freelance", "RECEITA"),
        ("Outros", "DESPESA"),
    ]
    for name, cat_type in defaults:
        create_category(user_id, name, cat_type)
    return True

def get_goals_by_user(user_id):
    query = "SELECT * FROM goals WHERE user_id = :user_id"
    return execute_query(query, {"user_id": int(user_id)}, fetch=True) or []

def create_goal(user_id, name, target_amount, deadline=None):
    query = "INSERT INTO goals (user_id, name, target_amount, current_amount, deadline, created_at) VALUES (:uid, :name, :target, 0.0, :deadline, datetime('now'))"
    return execute_query(query, {"uid": int(user_id), "name": name, "target": target_amount, "deadline": deadline})

def update_goal_progress(goal_id, amount_to_add):
    query_get = "SELECT current_amount FROM goals WHERE id = :id"
    res = execute_query(query_get, {"id": int(goal_id)}, fetch=True)
    if not res: return False

    new_total = float(res[0]['current_amount']) + float(amount_to_add)
    query_upd = "UPDATE goals SET current_amount = :amt WHERE id = :id"
    return execute_query(query_upd, {"amt": new_total, "id": int(goal_id)})
