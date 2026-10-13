"""Página de contas financeiras — CRUD (CU03, CU06)."""

import streamlit as st

from cinco_centavos.dashboard import components, theme
from cinco_centavos.dashboard.api_client import ApiError

ACCOUNT_TYPES = ["CORRENTE", "POUPANCA", "INVESTIMENTO", "ESPECIE", "CARTAO"]


def render(client) -> None:
    theme.page_header(
        eyebrow="Organização",
        title="Contas",
        subtitle="Conta corrente, poupança, carteira e cartões — tudo em um painel só.",
    )

    accounts = client.list_("/api/v1/users/me/accounts")
    if accounts:
        st.dataframe(
            [
                {
                    "ID": a["id"],
                    "Nome": a["name"],
                    "Tipo": a["type"],
                    "Saldo inicial": components.money(a["initial_balance"]),
                    "Saldo atual": components.money(a["balance"]),
                }
                for a in accounts
            ],
            use_container_width=True,
            hide_index=True,
        )
    else:
        theme.empty_state(
            "🏦",
            "Crie sua primeira conta",
            "Comece cadastrando onde seu dinheiro vive: pode ser uma conta corrente, carteira ou poupança.",
        )

    with st.form("new_account", clear_on_submit=True):
        st.subheader("Nova conta")
        name = st.text_input("Nome")
        type_ = st.selectbox("Tipo", ACCOUNT_TYPES)
        initial = st.number_input("Saldo inicial", value=0.0, step=100.0)
        if st.form_submit_button("Criar"):
            try:
                client.create(
                    "/api/v1/users/me/accounts",
                    {"name": name, "type": type_, "initial_balance": str(initial)},
                )
                st.success("Conta criada!")
                st.rerun()
            except ApiError as exc:
                st.error(str(exc))

    if accounts:
        with st.expander("Remover conta"):
            options = {f"{a['id']} — {a['name']}": a["id"] for a in accounts}
            label = st.selectbox("Conta", list(options))
            if st.button("Excluir", type="primary"):
                try:
                    client.delete(f"/api/v1/users/me/accounts/{options[label]}")
                    st.success("Conta removida.")
                    st.rerun()
                except ApiError as exc:
                    st.error(str(exc))
