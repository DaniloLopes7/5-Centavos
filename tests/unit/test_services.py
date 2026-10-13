"""Testes unitários da camada de serviços (regras de negócio)."""

import pytest
from datetime import date
from decimal import Decimal

from cinco_centavos.models import TransactionType
from cinco_centavos.schemas.account import AccountCreate
from cinco_centavos.schemas.analytics import FinancialSummary
from cinco_centavos.schemas.auth import UserRegister
from cinco_centavos.schemas.category import CategoryCreate
from cinco_centavos.schemas.goal import GoalCreate
from cinco_centavos.schemas.transaction import TransactionCreate, TransactionUpdate
from cinco_centavos.services import (
    AccountService,
    AnalyticsService,
    CategoryService,
    GoalService,
    TransactionService,
    UserService,
)
from cinco_centavos.services.exceptions import (
    BusinessRuleError,
    ConflictError,
    NotFoundError,
    UnauthorizedError,
)


def _register(db_session, email="a@b.com"):
    return UserService(db_session).register(
        UserRegister(name="Fulano", email=email, password="senha123")
    )


def _account(db_session, user_id):
    return AccountService(db_session).create_account(
        user_id,
        AccountCreate(name="Conta", type="CORRENTE", initial_balance=Decimal("1000")),
    )


def _transaction(db_session, user_id, account_id, category_id, type_, amount="100"):
    return TransactionService(db_session).create_transaction(
        user_id,
        TransactionCreate(
            account_id=account_id,
            category_id=category_id,
            description="Teste",
            amount=Decimal(amount),
            type=type_,
            date=date(2026, 1, 10),
        ),
    )


class TestUserService:
    def test_register_cria_usuario_com_categorias_padrao(self, db_session):
        user = _register(db_session)
        assert user.id is not None

        categories = CategoryService(db_session).list_categories(user.id)
        assert len(categories) == 10
        assert any(c.type.value == "RECEITA" for c in categories)
        assert any(c.type.value == "DESPESA" for c in categories)

    def test_register_rejeita_email_duplicado(self, db_session):
        _register(db_session)
        with pytest.raises(ConflictError):
            _register(db_session)

    def test_authenticate_sucesso_e_falha(self, db_session):
        _register(db_session, email="login@example.com")
        users = UserService(db_session)

        assert users.authenticate("login@example.com", "senha123") is not None
        with pytest.raises(UnauthorizedError):
            users.authenticate("login@example.com", "senha-errada")
        with pytest.raises(UnauthorizedError):
            users.authenticate("inexistente@example.com", "senha123")

    def test_senha_nunca_armazenada_em_texto_puro(self, db_session):
        user = _register(db_session)
        assert user.password_hash != "senha123"
        assert user.password_hash.startswith("$2")


class TestAccountService:
    def test_saldo_inicial_mais_receita_menos_despesa(self, db_session):
        user = _register(db_session)
        account = _account(db_session, user.id)
        categories = CategoryService(db_session).list_categories(user.id)
        receita = next(c for c in categories if c.type.value == "RECEITA")
        despesa = next(c for c in categories if c.type.value == "DESPESA")

        _transaction(db_session, user.id, account.id, receita.id, TransactionType.RECEITA, "500")
        _transaction(db_session, user.id, account.id, despesa.id, TransactionType.DESPESA, "200")

        result = AccountService(db_session).get_account(user.id, account.id)
        assert result.balance == Decimal("1300.00")

    def test_isolamento_conta_de_outro_usuario(self, db_session):
        user_a = _register(db_session, email="a@x.com")
        user_b = _register(db_session, email="b@x.com")
        account = _account(db_session, user_a.id)

        with pytest.raises(NotFoundError):
            AccountService(db_session).get_account(user_b.id, account.id)


class TestCategoryService:
    def test_nao_permite_categoria_duplicada(self, db_session):
        user = _register(db_session)
        service = CategoryService(db_session)
        service.create_category(user.id, CategoryCreate(name="Mercado", type="DESPESA"))
        with pytest.raises(ConflictError):
            service.create_category(user.id, CategoryCreate(name="Mercado", type="DESPESA"))


class TestTransactionService:
    def test_rejeita_categoria_de_tipo_incompativel(self, db_session):
        user = _register(db_session)
        account = _account(db_session, user.id)
        categories = CategoryService(db_session).list_categories(user.id)
        despesa = next(c for c in categories if c.type.value == "DESPESA")

        with pytest.raises(BusinessRuleError):
            _transaction(
                db_session, user.id, account.id, despesa.id, TransactionType.RECEITA
            )

    def test_rejeita_conta_inexistente(self, db_session):
        user = _register(db_session)
        categories = CategoryService(db_session).list_categories(user.id)
        receita = next(c for c in categories if c.type.value == "RECEITA")
        with pytest.raises(NotFoundError):
            _transaction(db_session, user.id, 999, receita.id, TransactionType.RECEITA)

    def test_update_recalcula_saldo(self, db_session):
        user = _register(db_session)
        account = _account(db_session, user.id)
        categories = CategoryService(db_session).list_categories(user.id)
        receita = next(c for c in categories if c.type.value == "RECEITA")
        tx = _transaction(db_session, user.id, account.id, receita.id, TransactionType.RECEITA)

        TransactionService(db_session).update_transaction(
            user.id, tx.id, TransactionUpdate(amount=Decimal("700"))
        )
        result = AccountService(db_session).get_account(user.id, account.id)
        assert result.balance == Decimal("1700.00")

    def test_delete_remove_e_afeta_saldo(self, db_session):
        user = _register(db_session)
        account = _account(db_session, user.id)
        categories = CategoryService(db_session).list_categories(user.id)
        despesa = next(c for c in categories if c.type.value == "DESPESA")
        tx = _transaction(db_session, user.id, account.id, despesa.id, TransactionType.DESPESA, "300")

        TransactionService(db_session).delete_transaction(user.id, tx.id)
        result = AccountService(db_session).get_account(user.id, account.id)
        assert result.balance == Decimal("1000.00")


class TestGoalService:
    def test_criacao_valida_valor_positivo(self, db_session):
        user = _register(db_session)
        with pytest.raises(Exception):
            GoalService(db_session).create_goal(
                user.id, GoalCreate(name="Meta", target_amount=Decimal("0"))
            )

    def test_progresso_acumulado(self, db_session):
        user = _register(db_session)
        service = GoalService(db_session)
        goal = service.create_goal(
            user.id, GoalCreate(name="Viagem", target_amount=Decimal("2000"))
        )
        service.add_progress(user.id, goal.id, Decimal("500"))
        updated = service.get_goal(user.id, goal.id)
        assert updated.current_amount == Decimal("500")


class TestAnalyticsService:
    def test_resumo_consolidado(self, db_session):
        user = _register(db_session)
        account = _account(db_session, user.id)
        categories = CategoryService(db_session).list_categories(user.id)
        receita = next(c for c in categories if c.type.value == "RECEITA")
        despesa = next(c for c in categories if c.type.value == "DESPESA")
        _transaction(db_session, user.id, account.id, receita.id, TransactionType.RECEITA, "1000")
        _transaction(db_session, user.id, account.id, despesa.id, TransactionType.DESPESA, "250")

        summary: FinancialSummary = AnalyticsService(db_session).get_financial_summary(user.id)
        assert summary.total_receitas == Decimal("1000.00")
        assert summary.total_despesas == Decimal("250.00")
        assert summary.saldo_atual == Decimal("1750.00")
        assert summary.taxa_poupanca == 75.0
        assert summary.total_contas == 1
        assert summary.total_transacoes == 2

    def test_evolucao_mensal_com_saldo_acumulado(self, db_session):
        from datetime import date as d

        user = _register(db_session)
        account = _account(db_session, user.id)
        categories = CategoryService(db_session).list_categories(user.id)
        receita = next(c for c in categories if c.type.value == "RECEITA")
        despesa = next(c for c in categories if c.type.value == "DESPESA")

        tx_service = TransactionService(db_session)
        tx_service.create_transaction(
            user.id,
            TransactionCreate(account_id=account.id, category_id=receita.id,
                              description="R janeiro", amount=Decimal("1000"),
                              type=TransactionType.RECEITA, date=d(2026, 1, 5)),
        )
        tx_service.create_transaction(
            user.id,
            TransactionCreate(account_id=account.id, category_id=despesa.id,
                              description="D janeiro", amount=Decimal("400"),
                              type=TransactionType.DESPESA, date=d(2026, 1, 20)),
        )
        tx_service.create_transaction(
            user.id,
            TransactionCreate(account_id=account.id, category_id=receita.id,
                              description="R fevereiro", amount=Decimal("1000"),
                              type=TransactionType.RECEITA, date=d(2026, 2, 5)),
        )

        evolution = AnalyticsService(db_session).get_monthly_evolution(user.id)
        assert [m.year_month for m in evolution] == ["2026-01", "2026-02"]
        assert evolution[0].saldo == Decimal("600")
        assert evolution[1].saldo == Decimal("1600")
