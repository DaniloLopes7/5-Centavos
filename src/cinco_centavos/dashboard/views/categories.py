"""Página de categorias — CRUD (CU10)."""

import streamlit as st

from cinco_centavos.dashboard import theme
from cinco_centavos.dashboard.api_client import ApiError


def render(client) -> None:
    theme.page_header(
        eyebrow="Organização",
        title="Categorias",
        subtitle="Agrupe seus gastos do seu jeito. A IA também aprende com elas.",
    )

    categories = client.list_("/api/v1/users/me/categories")
    if categories:
        st.dataframe(
            [{"ID": c["id"], "Nome": c["name"], "Tipo": c["type"]} for c in categories],
            use_container_width=True,
            hide_index=True,
        )
    else:
        theme.empty_state(
            "🏷️",
            "Nenhuma categoria por aqui",
            "Crie categorias como 'Mercado', 'Transporte' ou 'Lazer' para organizar seus lançamentos.",
        )

    col1, col2 = st.columns(2)
    with col1, st.form("new_category", clear_on_submit=True):
        st.subheader("Nova categoria")
        name = st.text_input("Nome")
        type_ = st.selectbox("Tipo", ["RECEITA", "DESPESA"])
        if st.form_submit_button("Criar"):
            try:
                client.create("/api/v1/users/me/categories", {"name": name, "type": type_})
                st.success("Categoria criada!")
                st.rerun()
            except ApiError as exc:
                st.error(str(exc))

    with col2:
        if categories:
            st.subheader("Remover")
            options = {f"{c['id']} — {c['name']} ({c['type']})": c["id"] for c in categories}
            label = st.selectbox("Categoria", list(options))
            if st.button("Excluir", type="primary"):
                try:
                    client.delete(f"/api/v1/users/me/categories/{options[label]}")
                    st.success("Removida.")
                    st.rerun()
                except ApiError as exc:
                    st.error(str(exc))
