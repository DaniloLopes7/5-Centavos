from typing import List, Optional
from decimal import Decimal
from datetime import datetime

from src.repositories import (
    UserRepository,
    AccountRepository,
    CategoryRepository,
    TransactionRepository,
    GoalRepository,
    AnalyticsRepository
)
from src.cinco_centavos.database import hash_password, check_password


class UserService:
    @staticmethod
    def register(name: str, email: str, password: str) -> Optional[dict]:
        if UserRepository.get_by_email(email):
            raise ValueError("Este e-mail já está cadastrado.")
        
        hashed_pw = hash_password(password)
        if UserRepository.create(name, email, hashed_pw):
            user = UserRepository.get_by_email(email)
            if user:
                # Create default categories
                UserService._create_default_categories(user['id'])
            return user
        return None

    @staticmethod
    def authenticate(email: str, password: str) -> Optional[dict]:
        user = UserRepository.get_by_email(email)
        if user and check_password(password, user['password_hash']):
            return user
        return None

    @staticmethod
    def get_by_id(user_id: int) -> Optional[dict]:
        return UserRepository.get_by_id(user_id)

    @staticmethod
    def _create_default_categories(user_id: int):
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
            CategoryRepository.create(user_id, name, cat_type)


class AccountService:
    @staticmethod
    def create(user_id: int, name: str, account_type: str, initial_balance: Decimal) -> bool:
        return AccountRepository.create(user_id, name, account_type, initial_balance)

    @staticmethod
    def get_user_accounts(user_id: int) -> List[dict]:
        accounts = AccountRepository.get_by_user(user_id)
        for acc in accounts:
            acc['current_balance'] = AccountService.calculate_balance(acc['id'])
        return accounts

    @staticmethod
    def get_account(account_id: int) -> Optional[dict]:
        acc = AccountRepository.get_by_id(account_id)
        if acc:
            acc['current_balance'] = AccountService.calculate_balance(account_id)
        return acc

    @staticmethod
    def calculate_balance(account_id: int) -> Decimal:
        account = AccountRepository.get_by_id(account_id)
        if not account:
            return Decimal('0.0')
        
        initial_balance = Decimal(str(account['initial_balance']))

        query_rev = """
            SELECT SUM(amount) as total FROM transactions
            WHERE account_id = :acc_id AND type = 'RECEITA'
        """
        from src.cinco_centavos.database import execute_query
        res_rev = execute_query(query_rev, {"acc_id": account_id}, fetch=True)
        revenues = Decimal(str(res_rev[0]['total'])) if res_rev and res_rev[0]['total'] else Decimal('0.0')

        query_exp = """
            SELECT SUM(amount) as total FROM transactions
            WHERE account_id = :acc_id AND type = 'DESPESA'
        """
        res_exp = execute_query(query_exp, {"acc_id": account_id}, fetch=True)
        expenses = Decimal(str(res_exp[0]['total'])) if res_exp and res_exp[0]['total'] else Decimal('0.0')

        return initial_balance + revenues - expenses

    @staticmethod
    def update(account_id: int, **kwargs) -> bool:
        return AccountRepository.update(account_id, **kwargs)

    @staticmethod
    def delete(account_id: int) -> bool:
        return AccountRepository.delete(account_id)


class CategoryService:
    @staticmethod
    def create(user_id: int, name: str, cat_type: str) -> bool:
        return CategoryRepository.create(user_id, name, cat_type)

    @staticmethod
    def get_user_categories(user_id: int) -> List[dict]:
        return CategoryRepository.get_by_user(user_id)

    @staticmethod
    def get_category(category_id: int) -> Optional[dict]:
        return CategoryRepository.get_by_id(category_id)

    @staticmethod
    def update(category_id: int, **kwargs) -> bool:
        return CategoryRepository.update(category_id, **kwargs)

    @staticmethod
    def delete(category_id: int) -> bool:
        return CategoryRepository.delete(category_id)


class TransactionService:
    @staticmethod
    def create(
        account_id: int,
        category_id: int,
        description: str,
        amount: Decimal,
        trans_type: str,
        date: datetime
    ) -> bool:
        # Validate account exists
        account = AccountRepository.get_by_id(account_id)
        if not account:
            raise ValueError("Conta não encontrada.")
        
        # Validate category exists
        category = CategoryRepository.get_by_id(category_id)
        if not category:
            raise ValueError("Categoria não encontrada.")
        
        # Validate category type matches transaction type
        if category['type'] != trans_type:
            raise ValueError(f"Tipo da categoria ({category['type']}) não corresponde ao tipo da transação ({trans_type}).")
        
        return TransactionRepository.create(account_id, category_id, description, amount, trans_type, date)

    @staticmethod
    def get_account_transactions(account_id: int) -> List[dict]:
        return TransactionRepository.get_by_account(account_id)

    @staticmethod
    def get_user_transactions(user_id: int) -> List[dict]:
        return TransactionRepository.get_by_user(user_id)

    @staticmethod
    def get_transaction(transaction_id: int) -> Optional[dict]:
        return TransactionRepository.get_by_id(transaction_id)

    @staticmethod
    def update(transaction_id: int, **kwargs) -> bool:
        # Validate category if being updated
        if 'category_id' in kwargs:
            category = CategoryRepository.get_by_id(kwargs['category_id'])
            if not category:
                raise ValueError("Categoria não encontrada.")
            if 'type' in kwargs and category['type'] != kwargs['type']:
                raise ValueError("Tipo da categoria não corresponde ao tipo da transação.")
            elif 'type' not in kwargs:
                trans = TransactionRepository.get_by_id(transaction_id)
                if trans and category['type'] != trans['type']:
                    raise ValueError("Tipo da categoria não corresponde ao tipo da transação.")
        
        return TransactionRepository.update(transaction_id, **kwargs)

    @staticmethod
    def delete(transaction_id: int) -> bool:
        return TransactionRepository.delete(transaction_id)


class GoalService:
    @staticmethod
    def create(user_id: int, name: str, target_amount: Decimal, deadline: Optional[datetime] = None) -> bool:
        return GoalRepository.create(user_id, name, target_amount, deadline)

    @staticmethod
    def get_user_goals(user_id: int) -> List[dict]:
        goals = GoalRepository.get_by_user(user_id)
        for g in goals:
            g['progress_percentage'] = (float(g['current_amount']) / float(g['target_amount'])) * 100 if g['target_amount'] > 0 else 0
        return goals

    @staticmethod
    def get_goal(goal_id: int) -> Optional[dict]:
        goal = GoalRepository.get_by_id(goal_id)
        if goal:
            goal['progress_percentage'] = (float(goal['current_amount']) / float(goal['target_amount'])) * 100 if goal['target_amount'] > 0 else 0
        return goal

    @staticmethod
    def update_progress(goal_id: int, amount: Decimal) -> bool:
        return GoalRepository.update_progress(goal_id, amount)

    @staticmethod
    def update(goal_id: int, **kwargs) -> bool:
        return GoalRepository.update(goal_id, **kwargs)

    @staticmethod
    def delete(goal_id: int) -> bool:
        return GoalRepository.delete(goal_id)


class AnalyticsService:
    @staticmethod
    def get_financial_summary(user_id: int) -> dict:
        return AnalyticsRepository.get_financial_summary(user_id)

    @staticmethod
    def get_category_summary(user_id: int) -> List[dict]:
        return AnalyticsRepository.get_category_summary(user_id)

    @staticmethod
    def get_monthly_summary(user_id: int) -> List[dict]:
        return AnalyticsRepository.get_monthly_summary(user_id)