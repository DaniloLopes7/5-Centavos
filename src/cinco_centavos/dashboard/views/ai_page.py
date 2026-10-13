"""Página de IA — insights, previsões, anomalias e classificação (CU16)."""

import pandas as pd
import streamlit as st

from cinco_centavos.dashboard import components, theme
from cinco_centavos.dashboard.api_client import ApiError


def render(client) -> None:
    theme.page_header(
        eyebrow="Inteligência",
        title="IA & Previsões",
        subtitle="Análises geradas a partir dos seus dados — sugestões, não decisões.",
    )

    if st.button("Treinar modelos com meus dados", type="primary"):
        with st.spinner("Treinando..."):
            status = client.create("/api/v1/ai/train", {})
        st.success(f"{status['message']} ({status['transactions_used']} transações)")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Insights personalizados")
        insights = client.list_("/api/v1/ai/insights")
        if insights.get("profile"):
            st.info(f"Perfil: {insights['profile']}")
        if insights["insights"]:
            for item in insights["insights"]:
                st.write(f"- {item}")
        else:
            theme.empty_state(
                "🤖",
                "Ainda sem insights",
                "Treine os modelos com suas transações (mínimo 8) para receber análises personalizadas.",
            )
        st.caption(insights["disclaimer"])

    with col2:
        st.subheader("Previsão de fluxo de caixa")
        prediction = client.list_("/api/v1/ai/cashflow-prediction")
        st.metric("Receitas previstas", components.money(prediction["expected_receitas"]))
        st.metric("Despesas previstas", components.money(prediction["expected_despesas"]))
        saldo = float(prediction["projected_balance"])
        st.metric(
            "Saldo projetado",
            components.money(prediction["projected_balance"]),
            delta="Positivo" if saldo >= 0 else "Negativo",
            delta_color="normal" if saldo >= 0 else "inverse",
        )
        st.caption(f"Base do cálculo: {prediction['basis']}")

    st.subheader("Classificador de transações")
    with st.form("predict", clear_on_submit=True):
        description = st.text_input("Descrição da transação")
        amount = st.number_input("Valor", min_value=0.01, step=10.0)
        type_ = st.selectbox("Tipo", ["DESPESA", "RECEITA"])
        if st.form_submit_button("Predizer categoria"):
            try:
                result = client.create(
                    "/api/v1/ai/predict-category",
                    {"description": description, "amount": str(amount), "type": type_},
                )
                st.success(
                    f"Categoria sugerida: **{result['category_name']}** "
                    f"(confiança: {result['confidence'] * 100:.0f}%)"
                )
            except ApiError as exc:
                st.error(str(exc))

    st.subheader("Gastos fora do padrão")
    anomalies = client.list_("/api/v1/ai/anomalies")
    if anomalies["total"]:
        st.dataframe(pd.DataFrame(anomalies["anomalies"]), use_container_width=True, hide_index=True)
    else:
        theme.empty_state(
            "✅",
            "Tudo dentro do padrão",
            "Nenhuma anomalia detectada nas suas despesas. Boa disciplina!",
        )
