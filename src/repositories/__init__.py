from typing import List, Optional
from decimal import Decimal
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from src.cinco_centavos.database import engine, execute_query


class UserRepository:
    @staticmethod
    def create(name: str, email: str, password_hash: str) -> bool:
        query = """
            INSERT INTO users (name, email, password_hash, created_at)
            VALUES (:name, :email, :pw, CURRENT_TIMESTAMP)
        """
        return execute_query(query, {"name": name, "email": email, "pw": password_hash})

    @staticmethod
    def get_by_email(email: str) -> Optional[dict]:
        query = "SELECT * FROM users WHERE email = :email"
        results = execute_query(query, {"email": email}, fetch=True)
        return results[0] if results else None

    @staticmethod
    def get_by_id(user_id: int) -> Optional[dict]:
        query = "SELECT * FROM users WHERE id = :user_id"
        results = execute_query(query, {"user_id": user_id}, fetch=True)
        return results[0] if results else None


class AccountRepository:
    @staticmethod
    def create(user_id: int, name: str, account_type: str, initial_balance: Decimal) -> bool:
        query = """
            INSERT INTO accounts (user_id, name, type, initial_balance, created_at)
            VALUES (:uid, :name, :type, :bal, CURRENT_TIMESTAMP)
        """
        return execute_query(query, {"uid": user_id, "name": name, "type": account_type, "bal": initial_balance})

    @staticmethod
    def get_by_user(user_id: int) -> List[dict]:
        query = "SELECT * FROM accounts WHERE user_id = :user_id"
        return execute_query(query, {"user_id": user_id}, fetch=True) or []

    @staticmethod
    def get_by_id(account_id: int) -> Optional[dict]:
        query = "SELECT * FROM accounts WHERE id = :account_id"
        results = execute_query(query, {"account_id": account_id}, fetch=True)
        return results[0] if results else None

    @staticmethod
    def update(account_id: int, **kwargs) -> bool:
        if not kwargs:
            return False
        set_clause = ", ".join([f"{k} = :{k}" for k in kwargs.keys()])
        query = f"UPDATE accounts SET {set_clause} WHERE id = :account_id"
        kwargs["account_id"] = account_id
        return execute_query(query, kwargs)

    @staticmethod
    def delete(account_id: int) -> bool:
        query = "DELETE FROM accounts WHERE id = :account_id"
        return execute_query(query, {"account_id": account_id})


class CategoryRepository:
    @staticmethod
    def create(user_id: int, name: str, cat_type: str) -> bool:
        query = "INSERT INTO categories (user_id, name, type) VALUES (:uid, :name, :type)"
        return execute_query(query, {"uid": user_id, "name": name, "type": cat_type})

    @staticmethod
    def get_by_user(user_id: int) -> List[dict]:
        query = "SELECT * FROM categories WHERE user_id = :user_id"
        return execute_query(query, {"user_id": user_id}, fetch=True) or []

    @staticmethod
    def get_by_id(category_id: int) -> Optional[dict]:
        query = "SELECT * FROM categories WHERE id = :category_id"
        results = execute_query(query, {"category_id": category_id}, fetch=True)
        return results[0] if results else None

    @staticmethod
    def update(category_id: int, **kwargs) -> bool:
        if not kwargs:
            return False
        set_clause = ", ".join([f"{k} = :{k}" for k in kwargs.keys()])
        query = f"UPDATE categories SET {set_clause} WHERE id = :category_id"
        kwargs["category_id"] = category_id
        return execute_query(query, kwargs)

    @staticmethod
    def delete(category_id: int) -> bool:
        query = "DELETE FROM categories WHERE id = :category_id"
        return execute_query(query, {"category_id": category_id})


class TransactionRepository:
    @staticmethod
    def create(
        account_id: int,
        category_id: int,
        description: str,
        amount: Decimal,
        trans_type: str,
        date: datetime
    ) -> bool:
        query = """
            INSERT INTO transactions (account_id, category_id, description, amount, type, date, created_at)
            VALUES (:acc_id, :cat_id, :desc, :amt, :type, :date, CURRENT_TIMESTAMP)
        """
        params = {
            "acc_id": account_id,
            "cat_id": category_id,
            "desc": description,
            "amt": amount,
            "type": trans_type,
            "date": date
        }
        return execute_query(query, params)

    @staticmethod
    def get_by_account(account_id: int) -> List[dict]:
        query = "SELECT * FROM transactions WHERE account_id = :acc_id ORDER BY date DESC"
        return execute_query(query, {"acc_id": account_id}, fetch=True) or []

    @staticmethod
    def get_by_user(user_id: int) -> List[dict]:
        query = """
            SELECT t.* FROM transactions t
            JOIN accounts a ON t.account_id = a.id
            WHERE a.user_id = :user_id
            ORDER BY t.date DESC
        """
        return execute_query(query, {"user_id": user_id}, fetch=True) or []

    @staticmethod
    def get_by_id(transaction_id: int) -> Optional[dict]:
        query = "SELECT * FROM transactions WHERE id = :transaction_id"
        results = execute_query(query, {"transaction_id": transaction_id}, fetch=True)
        return results[0] if results else None

    @staticmethod
    def update(transaction_id: int, **kwargs) -> bool:
        if not kwargs:
            return False
        set_clause = ", ".join([f"{k} = :{k}" for k in kwargs.keys()])
        query = f"UPDATE transactions SET {set_clause} WHERE id = :transaction_id"
        kwargs["transaction_id"] = transaction_id
        return execute_query(query, kwargs)

    @staticmethod
    def delete(transaction_id: int) -> bool:
        query = "DELETE FROM transactions WHERE id = :transaction_id"
        return execute_query(query, {"transaction_id": transaction_id})


class GoalRepository:
    @staticmethod
    def create(user_id: int, name: str, target_amount: Decimal, deadline: Optional[datetime] = None) -> bool:
        query = """
            INSERT INTO goals (user_id, name, target_amount, current_amount, deadline, created_at)
            VALUES (:uid, :name, :target, 0.0, :deadline, CURRENT_TIMESTAMP)
        """
        return execute_query(query, {"uid": user_id, "name": name, "target": target_amount, "deadline": deadline})

    @staticmethod
    def get_by_user(user_id: int) -> List[dict]:
        query = "SELECT * FROM goals WHERE user_id = :user_id"
        return execute_query(query, {"user_id": user_id}, fetch=True) or []

    @staticmethod
    def get_by_id(goal_id: int) -> Optional[dict]:
        query = "SELECT * FROM goals WHERE id = :goal_id"
        results = execute_query(query, {"goal_id": goal_id}, fetch=True)
        return results[0] if results else None

    @staticmethod
    def update(goal_id: int, **kwargs) -> bool:
        if not kwargs:
            return False
        set_clause = ", ".join([f"{k} = :{k}" for k in kwargs.keys()])
        query = f"UPDATE goals SET {set_clause} WHERE id = :goal_id"
        kwargs["goal_id"] = goal_id
        return execute_query(query, kwargs)

    @staticmethod
    def update_progress(goal_id: int, amount_to_add: Decimal) -> bool:
        query_get = "SELECT current_amount FROM goals WHERE id = :id"
        res = execute_query(query_get, {"id": goal_id}, fetch=True)
        if not res:
            return False
        new_total = float(res[0]['current_amount']) + float(amount_to_add)
        query_upd = "UPDATE goals SET current_amount = :amt WHERE id = :id"
        return execute_query(query_upd, {"amt": new_total, "id": goal_id})

    @staticmethod
    def delete(goal_id: int) -> bool:
        query = "DELETE FROM goals WHERE id = :goal_id"
        return execute_query(query, {"goal_id": goal_id})


class AnalyticsRepository:
    @staticmethod
    def get_financial_summary(user_id: int) -> dict:
        # Total receitas
        query_rev = """
            SELECT SUM(t.amount) as total FROM transactions t
            JOIN accounts a ON t.account_id = a.id
            WHERE a.user_id = :user_id AND t.type = 'RECEITA'
        """
        res_rev = execute_query(query_rev, {"user_id": user_id}, fetch=True)
        total_revenue = float(res_rev[0]['total']) if res_rev and res_rev[0]['total'] else 0.0

        # Total despesas
        query_exp = """
            SELECT SUM(t.amount) as total FROM transactions t
            JOIN accounts a ON t.account_id = a.id
            WHERE a.user_id = :user_id AND t.type = 'DESPESA'
        """
        res_exp = execute_query(query_exp, {"user_id": user_id}, fetch=True)
        total_expense = float(res_exp[0]['total']) if res_exp and res_exp[0]['total'] else 0.0

        # Contas
        query_acc = "SELECT COUNT(*) as count FROM accounts WHERE user_id = :user_id"
        res_acc = execute_query(query_acc, {"user_id": user_id}, fetch=True)
        accounts_count = res_acc[0]['count'] if res_acc else 0

        # Transações
        query_trans = """
            SELECT COUNT(*) as count FROM transactions t
            JOIN accounts a ON t.account_id = a.id
            WHERE a.user_id = :user_id
        """
        res_trans = execute_query(query_trans, {"user_id": user_id}, fetch=True)
        transactions_count = res_trans[0]['count'] if res_trans else 0

        return {
            "total_revenue": Decimal(str(total_revenue)),
            "total_expense": Decimal(str(total_expense)),
            "balance": Decimal(str(total_revenue - total_expense)),
            "accounts_count": accounts_count,
            "transactions_count": transactions_count
        }

    @staticmethod
    def get_category_summary(user_id: int) -> List[dict]:
        query = """
            SELECT
                c.id as category_id,
                c.name as category_name,
                c.type as category_type,
                SUM(t.amount) as total_amount,
                COUNT(t.id) as transactions_count
            FROM transactions t
            JOIN accounts a ON t.account_id = a.id
            JOIN categories c ON t.category_id = c.id
            WHERE a.user_id = :user_id
            GROUP BY c.id, c.name, c.type
            ORDER BY total_amount DESC
        """
        results = execute_query(query, {"user_id": user_id}, fetch=True) or []

        # Calculate percentages
        total = sum(float(r['total_amount']) for r in results) if results else 1
        for r in results:
            r['percentage'] = (float(r['total_amount']) / total) * 100 if total > 0 else 0

        return results

    @staticmethod
    def get_monthly_summary(user_id: int) -> List[dict]:
        query = """
            SELECT
                TO_CHAR(t.date, 'YYYY-MM') as month,
                SUM(CASE WHEN t.type = 'RECEITA' THEN t.amount ELSE 0 END) as revenue,
                SUM(CASE WHEN t.type = 'DESPESA' THEN t.amount ELSE 0 END) as expense
            FROM transactions t
            JOIN accounts a ON t.account_id = a.id
            WHERE a.user_id = :user_id
            GROUP BY TO_CHAR(t.date, 'YYYY-MM')
            ORDER BY month DESC
            LIMIT 12
        """
        results = execute_query(query, {"user_id": user_id}, fetch=True) or []
        for r in results:
            r['balance'] = float(r['revenue']) - float(r['expense'])
        return results