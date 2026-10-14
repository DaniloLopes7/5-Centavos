"""Leitura de configuração do ambiente ou dos Secrets do Streamlit Cloud."""

from __future__ import annotations

import os

import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError


def get_setting(name: str, default: str) -> str:
    """Prefere variável de ambiente e usa ``st.secrets`` como fallback."""
    value = os.getenv(name)
    if value:
        return value

    try:
        value = st.secrets[name]
    except (KeyError, FileNotFoundError, StreamlitSecretNotFoundError):
        return default
    return str(value)
