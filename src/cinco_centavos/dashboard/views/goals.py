"""Página de metas financeiras — criação, progresso e acompanhamento (CU12)."""

import streamlit as st

from cinco_centavos.dashboard import components, theme
from cinco_centavos.dashboard.api_client import ApiError


def render(client) -> None:
    theme.page_header(
        eyebrow="Objetivos",
        title="Metas financeiras",
        subtitle="Defina metas e acompanhe cada real se aproximando delas.",
    )

    goals = client.list_("/api/v1/goals")
    for goal in goals:
        progress = min(1.0, float(goal["current_amount"]) / float(goal["target_amount"]))
        deadline = goal.get("deadline") or "sem prazo"
        with st.container(border=True):
            st.subheader(f"🎯 {goal['name']}")
            st.progress(progress)
            st.caption(
                f"{components.money(goal['current_amount'])} de "
                f"{components.money(goal['target_amount'])} ({progress * 100:.1f}%) — "
                f"prazo: {deadline}"
            )
            col1, col2 = st.columns([1, 3])
            with col1:
                amount = st.number_input(
                    "Adicionar R$", min_value=0.0, step=50.0, key=f"prog_{goal['id']}"
                )
                if st.button("Adicionar", key=f"btn_{goal['id']}", type="primary") and amount > 0:
                    try:
                        client.create(
                            f"/api/v1/goals/{goal['id']}/progress", {"amount": str(amount)}
                        )
                        st.rerun()
                    except ApiError as exc:
                        st.error(str(exc))
            with col2:
                if st.button("Excluir meta", key=f"del_{goal['id']}"):
                    client.delete(f"/api/v1/goals/{goal['id']}")
                    st.rerun()

    if not goals:
        theme.empty_state(
            "🎯",
            "Nenhuma meta ainda",
            "Crie sua primeira meta — viagem, reserva de emergência, aquele presente...",
        )

    with st.form("new_goal", clear_on_submit=True):
        st.subheader("Nova meta")
        name = st.text_input("Nome da meta")
        target = st.number_input("Valor-alvo (R$)", min_value=0.01, step=100.0)
        deadline = st.date_input("Prazo (opcional)", value=None)
        if st.form_submit_button("Criar meta"):
            payload: dict = {"name": name, "target_amount": str(target)}
            if deadline:
                payload["deadline"] = deadline.isoformat()
            try:
                client.create("/api/v1/goals", payload)
                st.success("Meta criada!")
                st.rerun()
            except ApiError as exc:
                st.error(str(exc))
