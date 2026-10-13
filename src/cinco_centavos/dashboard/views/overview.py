"""Página Visão geral — indicadores e gráficos (CU11, CU15)."""

import datetime

import streamlit as st

from cinco_centavos.dashboard import components, theme


def render(client) -> None:
    theme.page_header(
        eyebrow="Análise",
        title="Visão geral",
        subtitle="Seu mês em números: o que entrou, o que saiu e quanto sobrou.",
    )

    col1, col2 = st.columns(2)
    start = col1.date_input("De", value=datetime.date.today().replace(day=1))
    end = col2.date_input("Até", value=datetime.date.today())
    params = {"start_date": start.isoformat(), "end_date": end.isoformat()}

    summary = client.list_("/api/v1/analytics/summary", params)
    components.metric_cards(summary)

    st.divider()
    components.expenses_pie(client.list_("/api/v1/analytics/categories", params))
    components.monthly_lines(client.list_("/api/v1/analytics/monthly"))
