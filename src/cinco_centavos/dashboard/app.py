"""Ponto de entrada do Dashboard Streamlit do 5 Centavos.

Autenticação: a landing page é a porta de entrada única. Cadastro/login lá
redirecionam para cá via ``?token=<jwt>``. O token é persistido em cookie
(``c5c_token``), assim a sessão sobrevive a F5 e novas abas (até o JWT expirar).

Execução::

    streamlit run src/cinco_centavos/dashboard/app.py
"""

from __future__ import annotations

import os

import streamlit as st

# Compatibilidade com dependências legadas que ainda usam @st.cache.
# O Streamlit 1.62+ removeu esse alias; o cookie manager usa o cache para dados.
if not hasattr(st, "cache"):
    st.cache = st.cache_data

from extra_streamlit_components import CookieManager

from cinco_centavos.dashboard import theme
from cinco_centavos.dashboard.api_client import ApiClient, ApiError

st.set_page_config(
    page_title="5 Centavos — Painel",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="expanded",
)
theme.inject()

LANDING_URL = os.getenv("LANDING_URL", "http://localhost:8080")
COOKIE_NAME = "c5c_token"

cookie_manager = CookieManager(key="c5c_cookie_manager")


def _set_token(token: str) -> None:
    """Persiste o token na sessão e no cookie (F5 não desloga mais)."""
    st.session_state["token"] = token
    cookie_manager.set(COOKIE_NAME, token)


def _clear_token() -> None:
    st.session_state.pop("token", None)
    cookie_manager.delete(COOKIE_NAME)


def _resolve_token() -> str | None:
    """Ordem: query param (vindo da landing) → sessão → cookie."""
    incoming = st.query_params.get("token")
    if incoming:
        _set_token(str(incoming))
        st.query_params.clear()
        return st.session_state["token"]

    token = st.session_state.get("token")
    if token:
        return token

    cookie_token = cookie_manager.get(COOKIE_NAME)
    if cookie_token:
        st.session_state["token"] = cookie_token
        return cookie_token

    if not st.session_state.get("_cookies_checked"):
        # Primeira montagem da sessão: o CookieManager ainda não hidratou.
        # Ele dispara um rerun automático logo em seguida com os cookies.
        st.session_state["_cookies_checked"] = True
        with st.spinner("Restaurando sua sessão…"):
            st.stop()
    return None


def _session_expired() -> None:
    _clear_token()
    theme.gate(LANDING_URL, "Sua sessão expirou. Entre novamente.")
    st.stop()


def _logout() -> None:
    _clear_token()
    theme.gate(LANDING_URL)
    st.stop()


NAV_ITEMS = {
    "🏠  Visão geral": "overview",
    "🏦  Contas": "accounts",
    "💸  Transações": "transactions",
    "🏷️  Categorias": "categories",
    "🎯  Metas": "goals",
    "🤖  IA & Previsões": "ai_page",
}


def _main() -> None:
    token = st.session_state.get("token")
    client = ApiClient(token)

    try:
        user = client.me()
    except ApiError as exc:
        if exc.status_code == 401:
            _session_expired()
        raise

    with st.sidebar:
        st.markdown(theme.brand(), unsafe_allow_html=True)
        st.markdown(
            f'<div class="c5c-user">👋 Olá, <strong>{user["name"]}</strong>!</div>',
            unsafe_allow_html=True,
        )
        page = st.radio("Menu", list(NAV_ITEMS), label_visibility="collapsed")
        st.divider()
        st.caption("100% grátis · Seus dados são seus")
        if st.button("Sair da conta", use_container_width=True):
            _logout()

    module_name = NAV_ITEMS[page]

    try:
        if module_name == "overview":
            from cinco_centavos.dashboard.views import overview

            overview.render(client)
        elif module_name == "accounts":
            from cinco_centavos.dashboard.views import accounts

            accounts.render(client)
        elif module_name == "transactions":
            from cinco_centavos.dashboard.views import transactions

            transactions.render(client)
        elif module_name == "categories":
            from cinco_centavos.dashboard.views import categories

            categories.render(client)
        elif module_name == "goals":
            from cinco_centavos.dashboard.views import goals

            goals.render(client)
        else:
            from cinco_centavos.dashboard.views import ai_page

            ai_page.render(client)
    except ApiError as exc:
        if exc.status_code == 401:
            _session_expired()
        raise


if _resolve_token():
    _main()
else:
    theme.gate(LANDING_URL)
