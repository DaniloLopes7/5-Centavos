"""Camada de Inteligência Artificial (RF17, CU16).

Cinco componentes especializados orquestrados pelo FinancialAdvisor:

* TransactionClassifier — RandomForest sobre TF-IDF classificando descrições em categorias;
* AnomalyDetector — IsolationForest identificando gastos atípicos;
* CashFlowPredictor — projeção de fluxo de caixa por médias móveis mensais;
* SpendingClusterer — K-Means agrupando perfis de comportamento de consumo;
* FinancialAdvisor — orquestrador que combina os modelos em insights acionáveis.

Regra de negócio (transparência): sugestões de IA não são decisões obrigatórias e
os fatores utilizados em cada análise são explicitados nas respostas.
"""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline

from cinco_centavos.core.logging import get_logger

logger = get_logger(__name__)

MIN_SAMPLES_TRAIN = 8
"""Mínimo de transações para treinar modelos com qualidade aceitável."""


# ---------------------------------------------------------------------------
# Utilidades de preparação de dados
# ---------------------------------------------------------------------------


def transactions_to_df(transactions: list[Any]) -> pd.DataFrame:
    """Converte transações ORM em DataFrame normalizado para análise/ML."""
    records = [
        {
            "id": t.id,
            "amount": float(t.amount),
            "type": t.type.value if hasattr(t.type, "value") else str(t.type),
            "description": str(t.description),
            "category_name": t.category.name,
            "date": pd.Timestamp(t.date),
        }
        for t in transactions
    ]
    if not records:
        return pd.DataFrame(
            columns=["id", "amount", "type", "description", "category_name", "date"]
        )
    df = pd.DataFrame(records)
    df["month"] = df["date"].dt.to_period("M").astype(str)
    df["day_of_month"] = df["date"].dt.day
    return df


# ---------------------------------------------------------------------------
# 1. Classificador de transações
# ---------------------------------------------------------------------------


class TransactionClassifier:
    """Classifica descrições de transações em categorias do usuário."""

    def __init__(self) -> None:
        self.pipeline = Pipeline(
            [
                ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
                (
                    "rf",
                    RandomForestClassifier(
                        n_estimators=100, random_state=42, class_weight="balanced"
                    ),
                ),
            ]
        )
        self.trained = False
        self.category_map: dict[str, str | None] = {}

    def train(self, df: pd.DataFrame) -> bool:
        """Treina com as transações do próprio usuário."""
        if len(df) < MIN_SAMPLES_TRAIN or df["category_name"].nunique() < 2:
            logger.info("classifier.not_enough_data", samples=len(df))
            return False
        self.pipeline.fit(df["description"], df["category_name"])
        self.trained = True
        return True

    def predict(self, description: str) -> tuple[str, float]:
        """Prediz a categoria de uma descrição e retorna (categoria, confiança)."""
        if not self.trained:
            return "Indefinida", 0.0
        probabilities = self.pipeline.predict_proba([description])[0]
        classes = self.pipeline.classes_
        best = int(np.argmax(probabilities))
        return str(classes[best]), round(float(probabilities[best]), 4)


# ---------------------------------------------------------------------------
# 2. Detector de anomalias
# ---------------------------------------------------------------------------


class AnomalyDetector:
    """Detecta gastos atípicos via Isolation Forest."""

    def __init__(self, contamination: float = 0.15) -> None:
        self.contamination = contamination
        self.model = IsolationForest(contamination=contamination, random_state=42)

    def detect(self, df: pd.DataFrame) -> pd.DataFrame:
        """Retorna o subconjunto de despesas detectadas como anômalas."""
        despesas = df[df["type"] == "DESPESA"].copy()
        if len(despesas) < MIN_SAMPLES_TRAIN:
            return despesas.iloc[0:0]

        features = despesas[["amount", "day_of_month"]].to_numpy(dtype=float)
        predictions = self.model.fit_predict(features)
        anomalies = despesas[predictions == -1].copy()

        if not anomalies.empty:
            limite = float(np.percentile(despesas["amount"], 90))
            anomalies["reason"] = anomalies["amount"].apply(
                lambda v: (
                    f"Valor R$ {v:,.2f} muito acima do padrão "
                    f"(p90 das despesas: R$ {limite:,.2f})"
                )
            )
        return anomalies


# ---------------------------------------------------------------------------
# 3. Previsor de fluxo de caixa
# ---------------------------------------------------------------------------


class CashFlowPredictor:
    """Projeta fluxo de caixa futuro usando médias móveis dos últimos meses."""

    def __init__(self, window: int = 3) -> None:
        self.window = window

    def predict(
        self, df: pd.DataFrame, period_months: int = 3
    ) -> tuple[Decimal, Decimal, str]:
        """Retorna (receitas_previstas, despesas_previstas, base_de_calculo)."""
        if df.empty:
            return Decimal(0), Decimal(0), "sem dados históricos"

        grouped = (
            df.groupby(["month", "type"])["amount"].sum().unstack(fill_value=0.0)
        )
        receitas = grouped.get("RECEITA", pd.Series(dtype=float)).tail(self.window)
        despesas = grouped.get("DESPESA", pd.Series(dtype=float)).tail(self.window)

        expected_receitas = float(receitas.mean()) * period_months if len(receitas) else 0.0
        expected_despesas = float(despesas.mean()) * period_months if len(despesas) else 0.0
        basis = (
            f"média dos últimos {max(1, min(self.window, len(grouped)))} meses "
            f"({len(df)} transações analisadas)"
        )
        return (
            Decimal(str(round(expected_receitas, 2))),
            Decimal(str(round(expected_despesas, 2))),
            basis,
        )


# ---------------------------------------------------------------------------
# 4. Agrupador de perfis de gasto
# ---------------------------------------------------------------------------


class SpendingClusterer:
    """Agrupa despesas em perfis de comportamento via K-Means."""

    def __init__(self, n_clusters: int = 2) -> None:
        self.n_clusters = n_clusters

    def profile(self, df: pd.DataFrame) -> str | None:
        """Retorna uma descrição do perfil predominante de gastos."""
        despesas = df[df["type"] == "DESPESA"]
        if len(despesas) < MIN_SAMPLES_TRAIN:
            return None

        features = despesas[["amount"]].to_numpy(dtype=float)
        k = min(self.n_clusters, len(despesas))
        labels = KMeans(n_clusters=k, random_state=42, n_init=10).fit_predict(features)

        means = [despesas["amount"][labels == i].mean() for i in range(k)]
        largest_cluster = int(np.argmax(np.bincount(labels)))
        media = float(np.nan_to_num(means[largest_cluster], nan=0.0))

        if media < 100:
            return "Consumo concentrado em despesas pequenas e frequentes"
        if media < 500:
            return "Consumo equilibrado com despesas de valor médio"
        return "Consumo concentrado em despesas de alto valor"


# ---------------------------------------------------------------------------
# 5. Conselheiro financeiro (orquestrador)
# ---------------------------------------------------------------------------


class FinancialAdvisor:
    """Combina os modelos de IA em insights acionáveis e transparentes."""

    def __init__(self) -> None:
        self.classifier = TransactionClassifier()
        self.detector = AnomalyDetector()
        self.predictor = CashFlowPredictor()
        self.clusterer = SpendingClusterer()

    def train(self, transactions: list[Any]) -> tuple[pd.DataFrame, int]:
        """Treina o classificador e retorna o DataFrame analisado."""
        df = transactions_to_df(transactions)
        self.classifier.train(df)
        return df, len(df)

    def generate_insights(self, df: pd.DataFrame) -> list[str]:
        """Gera insights com base nas regras + modelos treinados."""
        insights: list[str] = []
        if df.empty:
            return ["Sem dados suficientes para gerar insights ainda."]

        grouped = df.groupby(["month", "type"])["amount"].sum().unstack(fill_value=0.0)
        receitas = grouped.get("RECEITA", pd.Series(dtype=float))
        despesas = grouped.get("DESPESA", pd.Series(dtype=float))
        total_receitas = float(receitas.sum())
        total_despesas = float(despesas.sum())

        if total_receitas > 0:
            gasto_pct = round(total_despesas / total_receitas * 100, 1)
            insights.append(
                f"Você compromete {gasto_pct}% das suas receitas com despesas "
                f"(base: totais acumulados de {grouped.shape[0]} mes(es))."
            )
            if gasto_pct > 90:
                insights.append(
                    "Atenção: despesas acima de 90% das receitas deixam pouca "
                    "margem para poupança. Revise as maiores categorias de gasto."
                )

        maior_categoria = (
            df[df["type"] == "DESPESA"].groupby("category_name")["amount"].sum()
        )
        if not maior_categoria.empty:
            nome = maior_categoria.idxmax()
            valor = float(maior_categoria.max())
            insights.append(
                f"Sua maior categoria de despesa é '{nome}' com R$ {valor:,.2f} "
                "(base: soma de despesas por categoria)."
            )

        anomalies = self.detector.detect(df)
        if not anomalies.empty:
            insights.append(
                f"{len(anomalies)} transação(ões) de despesa fora do padrão "
                "detectada(s) — verifique em /api/v1/ai/anomalies "
                "(base: Isolation Forest sobre valor e dia do mês)."
            )

        profile = self.clusterer.profile(df)
        if profile:
            insights.append(
                f"Perfil de consumo: {profile} (base: K-Means sobre os valores das despesas)."
            )

        insights.append(
            f"Última análise realizada em {datetime.now(UTC).strftime('%Y-%m-%d %H:%M UTC')}."
        )
        return insights


__all__ = [
    "AnomalyDetector",
    "CashFlowPredictor",
    "FinancialAdvisor",
    "SpendingClusterer",
    "TransactionClassifier",
    "transactions_to_df",
]
