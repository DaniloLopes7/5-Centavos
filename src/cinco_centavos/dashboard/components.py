"""Componentes visuais reutilizáveis do dashboard (design system 5 Centavos)."""

from decimal import Decimal

import pandas as pd
import plotly.express as px
import streamlit as st

from cinco_centavos.dashboard import theme

# Sequência de cores dos gráficos: grafite, amarelo e tons quentes
# (verde e coral ficam exclusivos de entrada/saída, nunca decoração).
CHART_SEQUENCE = ["#F5A800", "#1A1A1A", "#F2C94C", "#9B8AFB", "#F2994A", "#6B6B66"]


def money(value: float | Decimal | str | int) -> str:
    """Formata valor monetário em padrão brasileiro."""
    return f"R$ {float(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def metric_cards(summary: dict) -> None:
    """Cartões de indicadores principais do resumo financeiro."""
    saldo = float(summary["saldo_atual"])
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Receitas", money(summary["total_receitas"]))
    col2.metric("Despesas", money(summary["total_despesas"]))
    col3.metric(
        "Saldo atual",
        money(summary["saldo_atual"]),
        delta="No azul" if saldo >= 0 else "No vermelho",
        delta_color="normal" if saldo >= 0 else "inverse",
    )
    col4.metric("Taxa de poupança", f"{summary['taxa_poupanca']:.1f}%")


def expenses_pie(breakdown: list[dict]) -> None:
    """Gráfico de pizza — despesas por categoria."""
    rows = [r for r in breakdown if r["type"] == "DESPESA"]
    if not rows:
        theme.empty_state(
            "📊",
            "Ainda sem despesas no período",
            "Quando você registrar seus gastos, mostramos aqui o gráfico por categoria.",
        )
        return
    df = pd.DataFrame(rows)
    fig = px.pie(
        df,
        names="category",
        values="total",
        title="Despesas por categoria",
        color_discrete_sequence=CHART_SEQUENCE,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#1A1A1A"),
    )
    st.plotly_chart(fig, use_container_width=True)


def monthly_lines(evolution: list[dict]) -> None:
    """Gráfico de linhas — evolução mensal de receitas, despesas e saldo."""
    if not evolution:
        theme.empty_state(
            "📈",
            "Sem histórico mensal ainda",
            "Depois de alguns dias lançando transações, a evolução do seu dinheiro aparece aqui.",
        )
        return
    df = pd.DataFrame(evolution)
    df = df.melt(
        id_vars="year_month",
        value_vars=["receitas", "despesas", "saldo"],
        var_name="Métrica",
        value_name="Valor",
    )
    # Verde = entrada, coral = saída, grafite = saldo (regra do design system)
    color_map = {"receitas": "#2E9E6B", "despesas": "#E5484D", "saldo": "#1A1A1A"}
    fig = px.line(
        df,
        x="year_month",
        y="Valor",
        color="Métrica",
        markers=True,
        title="Evolução mensal",
        color_discrete_map=color_map,
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#1A1A1A"),
    )
    st.plotly_chart(fig, use_container_width=True)
