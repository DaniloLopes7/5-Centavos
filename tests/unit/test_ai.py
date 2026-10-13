"""Testes unitários dos modelos de IA."""

from datetime import date
from decimal import Decimal
from types import SimpleNamespace

import pytest

from cinco_centavos.ai import (
    AnomalyDetector,
    CashFlowPredictor,
    FinancialAdvisor,
    SpendingClusterer,
    TransactionClassifier,
    transactions_to_df,
)


def _fake_transaction(id_, description, amount, type_, category_name, date_):
    return SimpleNamespace(
        id=id_,
        amount=Decimal(amount),
        type=SimpleNamespace(value=type_),
        description=description,
        category=SimpleNamespace(name=category_name),
        date=date_,
    )


def make_transactions():
    """Gera transações sintéticas suficientes para treino dos modelos."""
    base = []
    for month in range(1, 5):
        base.append(_fake_transaction(len(base)+1, "salario mensal", "3000", "RECEITA", "Salário", date(2026, month, 5)))
        base.append(_fake_transaction(len(base)+1, "supermercado extra", "450", "DESPESA", "Alimentação", date(2026, month, 8)))
        base.append(_fake_transaction(len(base)+1, "mercado padaria", "200", "DESPESA", "Alimentação", date(2026, month, 15)))
        base.append(_fake_transaction(len(base)+1, "aluguel", "1500", "DESPESA", "Moradia", date(2026, month, 5)))
        base.append(_fake_transaction(len(base)+1, "combustivel posto", "220", "DESPESA", "Transporte", date(2026, month, 12)))
    base.append(_fake_transaction(len(base)+1, "gasto emergencial raro", "4500", "DESPESA", "Alimentação", date(2026, 4, 20)))
    return base


class TestTransactionClassifier:
    def test_treina_e_prediz_categoria(self):
        classifier = TransactionClassifier()
        df = transactions_to_df(make_transactions())
        assert classifier.train(df)

        name, confidence = classifier.predict("compra no supermercado")
        assert name == "Alimentação"
        assert 0 < confidence <= 1

    def test_sem_dados_retorna_indefinida(self):
        classifier = TransactionClassifier()
        assert not classifier.train(transactions_to_df([]))
        name, confidence = classifier.predict("qualquer coisa")
        assert name == "Indefinida"
        assert confidence == 0.0


class TestAnomalyDetector:
    def test_detecta_gasto_atipico(self):
        detector = AnomalyDetector(contamination=0.2)
        df = transactions_to_df(make_transactions())
        anomalies = detector.detect(df)
        assert len(anomalies) >= 1
        assert float(anomalies["amount"].max()) == pytest.approx(4500.0)

    def test_sem_dados_retorna_vazio(self):
        assert AnomalyDetector().detect(transactions_to_df([])).empty


class TestCashFlowPredictor:
    def test_projecao_baseada_em_media(self):
        predictor = CashFlowPredictor()
        df = transactions_to_df(make_transactions())
        receitas, despesas, basis = predictor.predict(df, period_months=2)
        assert receitas == Decimal("6000.0")  # média 3000/mês x 2 meses
        assert despesas > 0
        assert "últimos" in basis

    def test_sem_dados_retorna_zeros(self):
        receitas, despesas, _ = CashFlowPredictor().predict(transactions_to_df([]))
        assert receitas == 0 and despesas == 0


class TestSpendingClusterer:
    def test_retorna_perfil_legivel(self):
        df = transactions_to_df(make_transactions())
        profile = SpendingClusterer().profile(df)
        assert profile is not None
        assert "Consumo" in profile


class TestFinancialAdvisor:
    def test_insights_contem_transparencia(self):
        advisor = FinancialAdvisor()
        transactions = make_transactions()
        df, count = advisor.train(transactions)
        assert count == len(transactions)

        insights = advisor.generate_insights(df)
        assert insights
        assert any("maior categoria" in i for i in insights)
        assert any("receitas" in i for i in insights)
