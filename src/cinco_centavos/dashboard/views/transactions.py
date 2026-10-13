"""Página de transações — histórico e CRUD (CU04, CU05, CU07, CU08, CU09)."""

import datetime

import pandas as pd
import streamlit as st

from cinco_centavos.dashboard import components, theme
from cinco_centavos.dashboard.api_client import ApiError


def _resolved_names(accounts: list[dict], categories: list[dict]) -> tuple[dict, dict]:
    account_names = {a["id"]: a["name"] for a in accounts}
    category_names = {c["id"]: c["name"] for c in categories}
    return account_names, category_names


def render(client) -> None:
    theme.page_header(
        eyebrow="Movimentações",
        title="Transações",
        subtitle="Registre receitas e despesas em segundos — a IA ajuda a categorizar.",
    )

    accounts = client.list_("/api/v1/users/me/accounts")
    categories = client.list_("/api/v1/users/me/categories")
    account_names, category_names = _resolved_names(accounts, categories)

    tab_list, tab_new = st.tabs(["Histórico", "Nova transação"])

    with tab_list:
        c1, c2, c3 = st.columns(3)
        account_filter = c1.selectbox(
            "Conta", ["Todas"] + [a["name"] for a in accounts]
        )
        type_filter = c2.selectbox("Tipo", ["Todos", "RECEITA", "DESPESA"])
        params: dict = {}
        if account_filter != "Todas":
            params["account_id"] = next(a["id"] for a in accounts if a["name"] == account_filter)
        if type_filter != "Todos":
            params["type"] = type_filter

        txs = client.list_("/api/v1/transactions", params)
        if txs:
            df = pd.DataFrame(txs)
            df["conta"] = df["account_id"].map(account_names)
            df["categoria"] = df["category_id"].map(category_names)
            df["valor"] = df["amount"].apply(components.money)
            st.dataframe(
                df[["id", "date", "description", "categoria", "conta", "type", "valor"]],
                use_container_width=True,
                hide_index=True,
            )
            with st.expander("Excluir transação"):
                labels = {f"#{t['id']} — {t['description']}": t["id"] for t in txs}
                chosen = st.selectbox("Transação", list(labels))
                if st.button("Excluir", type="primary"):
                    try:
                        client.delete(f"/api/v1/transactions/{labels[chosen]}")
                        st.success("Removida.")
                        st.rerun()
                    except ApiError as exc:
                        st.error(str(exc))
        else:
            theme.empty_state(
                "💸",
                "Nenhuma transação encontrada",
                "Adicione seu primeiro gasto na aba 'Nova transação' — leva poucos segundos.",
            )

    with tab_new:
        if not accounts or not categories:
            theme.empty_state(
                "🧾",
                "Antes de registrar, crie uma conta e uma categoria",
                "É rapidinho: vá até as páginas 'Contas' e 'Categorias' para configurar o básico.",
            )
            return
        with st.form("new_transaction", clear_on_submit=True):
            account_label = st.selectbox("Conta", [a["name"] for a in accounts])
            type_ = st.radio("Tipo", ["RECEITA", "DESPESA"], horizontal=True)
            compatible = [c for c in categories if c["type"] == type_]
            category_label = st.selectbox("Categoria", [c["name"] for c in compatible])
            description = st.text_input("Descrição")
            amount = st.number_input("Valor (R$)", min_value=0.01, step=10.0)
            tx_date = st.date_input("Data", value=datetime.date.today())
            if st.form_submit_button("Registrar"):
                category = next(c for c in compatible if c["name"] == category_label)
                account = next(a for a in accounts if a["name"] == account_label)
                try:
                    client.create(
                        "/api/v1/transactions",
                        {
                            "account_id": account["id"],
                            "category_id": category["id"],
                            "description": description,
                            "amount": str(amount),
                            "type": type_,
                            "date": tx_date.isoformat(),
                        },
                    )
                    st.success("Transação registrada!")
                    st.rerun()
                except ApiError as exc:
                    st.error(str(exc))
