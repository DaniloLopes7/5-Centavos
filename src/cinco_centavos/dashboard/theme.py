"""Design system 5 Centavos injetado no Streamlit.

Aplica a identidade "Clareza que vale ouro" (mesma das variáveis CSS da
landing em landing/styles.css) sobre os componentes nativos do Streamlit.
"""

from __future__ import annotations

import streamlit as st

# Paleta (espelho das CSS custom properties da landing)
PRIMARY = "#FFC72C"
PRIMARY_DEEP = "#F5A800"
PRIMARY_SOFT = "#FFF4CC"
TEXT = "#1A1A1A"
TEXT_SECONDARY = "#6B6B66"
BORDER = "#ECE9E0"
BG = "#FFFFFF"
BG_ALT = "#FAF8F2"
POSITIVE = "#2E9E6B"
NEGATIVE = "#E5484D"

_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700;800&family=Inter:wght@400;500;600;700&display=swap');

/* ---------- Base ---------- */
.stApp {{
  background: {BG_ALT};
  font-family: 'Inter', sans-serif;
  color: {TEXT};
}}
html, body, [data-testid="stAppViewContainer"] * {{
  font-family: 'Inter', sans-serif;
}}
h1, h2, h3, h4, h5 {{
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-weight: 800 !important;
  letter-spacing: -0.02em;
  color: {TEXT};
}}

/* ---------- Números tabulares ---------- */
[data-testid="stMetricValue"], [data-testid="stDataFrame"] td {{
  font-variant-numeric: tabular-nums;
}}

/* ---------- Área de conteúdo ---------- */
[data-testid="stAppViewContainer"] > .main .block-container {{
  padding-top: 3.5rem;
  max-width: 1180px;
}}

/* ---------- Cabeçalho nativo (hamburger) ---------- */
[data-testid="stHeader"] {{
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid {BORDER};
}}

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {{
  background: {BG};
  border-right: 1px solid {BORDER};
  min-width: 280px;
}}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
  color: {TEXT};
}}

/* Navegação multipage automática do Streamlit: desativada —
   a pasta de telas se chama `views/` (não `pages/`) por isso mesmo.
   Este seletor é proteção extra caso a convenção mude. */
[data-testid="stSidebarNav"],
[data-testid="stSidebarNavItems"] {{
  display: none !important;
}}

/* ---------- Botões de abrir/fechar a sidebar ----------
   O ícone nativo usa a fonte Material Symbols; quando ela não carrega,
   aparece o texto cru ("double_arrow_right"). Substituímos por um glyph
   próprio, sempre visível e com estilo do design system. */
[data-testid="stSidebarCollapseButton"] [data-testid="stIconMaterial"],
[data-testid="collapsedControl"] [data-testid="stIconMaterial"] {{
  font-family: 'Inter', sans-serif !important;
  font-size: 0 !important;
  line-height: 0 !important;
}}
[data-testid="stSidebarCollapseButton"] [data-testid="stIconMaterial"] span,
[data-testid="collapsedControl"] [data-testid="stIconMaterial"] span {{
  display: none !important;
}}
[data-testid="stSidebarCollapseButton"] [data-testid="stIconMaterial"]::after {{
  content: "‹";
  font-size: 1.7rem;
  line-height: 1;
  color: {TEXT_SECONDARY};
}}
[data-testid="collapsedControl"] [data-testid="stIconMaterial"]::after {{
  content: "☰";
  font-size: 1.4rem;
  line-height: 1;
  color: {TEXT};
}}
[data-testid="stSidebarCollapseButton"]:hover [data-testid="stIconMaterial"]::after {{
  color: {PRIMARY_DEEP};
}}
[data-testid="collapsedControl"]:hover [data-testid="stIconMaterial"]::after {{
  color: {PRIMARY_DEEP};
}}
[data-testid="collapsedControl"] button {{
  background: {PRIMARY} !important;
  border: 1px solid {BORDER} !important;
  border-radius: 12px !important;
  width: 40px; height: 40px;
  box-shadow: 0 8px 20px rgba(245, 168, 0, 0.3) !important;
}}

/* ---------- Menu (radio → nav pills) ---------- */
[data-testid="stSidebar"] [data-testid="stRadio"] > label {{ display: none; }}
[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] {{
  display: flex;
  flex-direction: column;
  gap: 4px;
}}
[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label {{
  display: flex;
  align-items: center;
  padding: 11px 16px !important;
  border-radius: 14px;
  cursor: pointer;
  transition: background 0.18s ease, box-shadow 0.18s ease, transform 0.18s ease;
  border: 1px solid transparent;
}}
[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label:hover {{
  background: {PRIMARY_SOFT};
}}
[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label:active {{
  transform: scale(0.985);
}}
/* esconde o círculo do radio */
[data-testid="stSidebar"] [data-testid="stRadio"] label > div:first-child {{
  display: none !important;
}}
/* item ativo: amarelo, texto grafite (regra da paleta) */
[data-testid="stSidebar"] [data-testid="stRadio"] label:has([data-checked="true"]),
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {{
  background: linear-gradient(135deg, {PRIMARY}, {PRIMARY_DEEP}) !important;
  box-shadow: 0 8px 20px rgba(245, 168, 0, 0.32);
}}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) p,
[data-testid="stSidebar"] [data-testid="stRadio"] label:has([data-checked="true"]) p {{
  font-weight: 700 !important;
  color: {TEXT} !important;
}}

/* ---------- Marca ---------- */
.c5c-brand {{
  display: flex;
  align-items: center;
  gap: 10px;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-weight: 800;
  font-size: 1.35rem;
  color: {TEXT};
  padding: 6px 2px 2px;
}}
.c5c-brand .coin {{
  width: 42px; height: 42px;
  display: grid; place-items: center;
  background: linear-gradient(145deg, {PRIMARY}, {PRIMARY_DEEP});
  border-radius: 14px;
  font-size: 1.3rem;
  box-shadow: 0 10px 24px rgba(245, 168, 0, 0.35);
}}
.c5c-user {{
  margin: 10px 0 18px;
  padding: 12px 16px;
  background: {PRIMARY_SOFT};
  border: 1px solid #F3E3AC;
  border-radius: 14px;
  font-size: 0.92rem;
}}
.c5c-user strong {{ font-family: 'Plus Jakarta Sans', sans-serif; }}

/* ---------- Headers de página ---------- */
.c5c-header {{ margin-bottom: 8px; }}
.c5c-eyebrow {{
  font-weight: 700;
  font-size: 0.75rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: {PRIMARY_DEEP};
  font-family: 'Inter', sans-serif;
}}
.c5c-title {{
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 2.1rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  line-height: 1.15;
  color: {TEXT};
  margin: 2px 0 4px;
}}
.c5c-sub {{ color: {TEXT_SECONDARY}; font-size: 1rem; margin-bottom: 20px; }}
.c5c-mark {{
  background: linear-gradient(180deg, transparent 55%, {PRIMARY} 55%, {PRIMARY} 96%, rgba(255,199,44,0.55) 100%);
  border-radius: 6px;
  padding-inline: 2px;
}}

/* ---------- Métricas → cards ---------- */
[data-testid="stMetric"] {{
  background: {BG};
  border: 1px solid {BORDER};
  border-radius: 18px;
  padding: 18px 20px;
  box-shadow: 0 14px 34px rgba(245, 168, 0, 0.08);
}}
[data-testid="stMetricLabel"] {{ color: {TEXT_SECONDARY}; font-weight: 500; }}
[data-testid="stMetricValue"] {{
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-weight: 800;
  color: {TEXT};
}}

/* ---------- Botões ---------- */
.stButton > button, .stFormSubmitButton > button,
[data-testid="stFormSubmitButton"] > button {{
  border-radius: 999px !important;
  font-weight: 600 !important;
  border: 1px solid {BORDER} !important;
  background: {BG} !important;
  color: {TEXT} !important;
  padding: 0.55rem 1.4rem !important;
  transition: transform .18s ease, box-shadow .18s ease !important;
}}
.stButton > button:hover, .stFormSubmitButton > button:hover,
[data-testid="stFormSubmitButton"] > button:hover {{
  transform: translateY(-2px);
  box-shadow: 0 10px 26px rgba(245, 168, 0, 0.16);
}}
.stButton > button[kind="primary"],
.stFormSubmitButton > button[kind="primary"],
[data-testid="stFormSubmitButton"] > button[kind="primary"],
.stButton > button[kind="primaryFormSubmit"] {{
  background: linear-gradient(135deg, {PRIMARY}, {PRIMARY_DEEP}) !important;
  border: 0 !important;
  color: {TEXT} !important;
  box-shadow: 0 10px 26px rgba(245, 168, 0, 0.35) !important;
}}

/* ---------- Inputs ---------- */
[data-baseweb="input"] > div,
[data-baseweb="select"] > div,
[data-baseweb="base-input"],
.stDateInput input,
.stNumberInput input {{
  border-radius: 14px !important;
  background: {BG} !important;
  border-color: {BORDER} !important;
}}
[data-baseweb="input"] input:focus, [data-baseweb="select"] [aria-expanded="true"] {{
  border-color: {PRIMARY_DEEP} !important;
  box-shadow: 0 0 0 3px rgba(255, 199, 44, 0.28) !important;
}}

/* ---------- Radio / Tabs ---------- */
[data-testid="stRadio"] label p {{ font-weight: 500; }}
[data-testid="stRadio"] [data-checked="true"] p {{ font-weight: 700; }}
[data-testid="stTabs"] [data-baseweb="tab-list"] {{
  gap: 8px;
  background: {BG};
  border: 1px solid {BORDER};
  border-radius: 999px;
  padding: 6px;
  width: fit-content;
}}
[data-testid="stTabs"] [data-baseweb="tab"] {{
  border-radius: 999px;
  padding: 8px 22px;
  font-weight: 600;
  color: {TEXT_SECONDARY};
}}
[data-testid="stTabs"] [aria-selected="true"] {{
  background: {TEXT} !important;
  color: #fff !important;
}}
[data-testid="stTabs"] [data-baseweb="tab-highlight"] {{ display: none; }}

/* ---------- Form / Expander / Containers ---------- */
[data-testid="stForm"], [data-testid="stExpander"] {{
  background: {BG};
  border: 1px solid {BORDER};
  border-radius: 20px;
  box-shadow: 0 14px 34px rgba(245, 168, 0, 0.07);
}}
[data-testid="stExpander"] details {{
  border-radius: 20px;
}}
[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlock"] > [style*="border"] {{
  border-radius: 20px !important;
  border-color: {BORDER} !important;
}}

/* ---------- Dataframe ---------- */
[data-testid="stDataFrame"] {{
  background: {BG};
  border: 1px solid {BORDER};
  border-radius: 18px;
  overflow: hidden;
}}

/* ---------- Progress ---------- */
[data-testid="stProgressBar"] > div > div {{
  background: linear-gradient(90deg, {PRIMARY_DEEP}, {PRIMARY}) !important;
}}

/* ---------- Alertas ---------- */
[data-testid="stAlert"] {{
  border-radius: 16px;
  border: 1px solid {BORDER};
}}

/* ---------- Divider ---------- */
hr {{ border-color: {BORDER}; }}

/* ---------- Empty state ---------- */
.c5c-empty {{
  text-align: center;
  padding: 44px 28px;
  background: {BG};
  border: 1px dashed {BORDER};
  border-radius: 20px;
}}
.c5c-empty .icon {{
  width: 64px; height: 64px;
  margin: 0 auto 14px;
  display: grid; place-items: center;
  background: {PRIMARY_SOFT};
  border-radius: 20px;
  font-size: 2rem;
}}
.c5c-empty h3 {{
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 1.25rem;
  margin-bottom: 6px;
}}
.c5c-empty p {{ color: {TEXT_SECONDARY}; font-size: 0.95rem; max-width: 400px; margin: 0 auto; }}

/* ---------- Gate (tela "entre pela landing") ---------- */
.c5c-gate {{
  max-width: 460px;
  margin: 9vh auto 0;
  text-align: center;
  background: {BG};
  border: 1px solid {BORDER};
  border-radius: 24px;
  padding: 48px 40px;
  box-shadow: 0 24px 60px rgba(245, 168, 0, 0.14);
}}
.c5c-gate .coin {{
  width: 76px; height: 76px;
  margin: 0 auto 18px;
  display: grid; place-items: center;
  background: linear-gradient(145deg, {PRIMARY}, {PRIMARY_DEEP});
  border-radius: 24px;
  font-size: 2.2rem;
  box-shadow: 0 16px 40px rgba(245, 168, 0, 0.35);
}}
.c5c-gate h1 {{
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 1.9rem;
  font-weight: 800;
  margin-bottom: 10px;
}}
.c5c-gate p {{ color: {TEXT_SECONDARY}; margin-bottom: 24px; }}
.c5c-gate a.c5c-btn {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: linear-gradient(135deg, {PRIMARY}, {PRIMARY_DEEP});
  color: {TEXT};
  font-weight: 700;
  text-decoration: none;
  padding: 15px 34px;
  border-radius: 999px;
  box-shadow: 0 12px 30px rgba(245, 168, 0, 0.38);
  transition: transform .18s ease;
}}
.c5c-gate a.c5c-btn:hover {{ transform: translateY(-2px); }}
.c5c-gate .micro {{ margin-top: 16px; font-size: 0.82rem; color: {TEXT_SECONDARY}; }}

/* ---------- Acessibilidade / movimento ---------- */
@media (prefers-reduced-motion: reduce) {{
  * {{ transition-duration: 0.01ms !important; animation-duration: 0.01ms !important; }}
}}
</style>
"""


def inject() -> None:
    """Injeta o CSS do design system na página (chamar após set_page_config)."""
    st.markdown(_CSS, unsafe_allow_html=True)


def brand() -> str:
    """Logo 5 Centavos (HTML) para a sidebar e telas."""
    return (
        '<div class="c5c-brand">'
        '<div class="coin">🪙</div>'
        "<div>5 Centavos</div>"
        "</div>"
    )


def page_header(eyebrow: str, title: str, subtitle: str | None = None, highlight: str | None = None) -> None:
    """Cabeçalho padrão de página: kicker amarelo + título com marca-texto."""
    title_html = title
    if highlight:
        title_html = title.replace(highlight, f'<span class="c5c-mark">{highlight}</span>')
    st.markdown(
        f'<div class="c5c-header">'
        f'<div class="c5c-eyebrow">{eyebrow}</div>'
        f'<div class="c5c-title">{title_html}</div>'
        + (f'<p class="c5c-sub">{subtitle}</p>' if subtitle else "")
        + "</div>",
        unsafe_allow_html=True,
    )


def empty_state(icon: str, title: str, text: str) -> None:
    """Estado vazio amigável (ilustração + mensagem), padrão da landing."""
    st.markdown(
        f'<div class="c5c-empty">'
        f'<div class="icon">{icon}</div>'
        f"<h3>{title}</h3>"
        f"<p>{text}</p>"
        "</div>",
        unsafe_allow_html=True,
    )


def gate(landing_url: str, message: str | None = None) -> None:
    """Tela exibida quando não há sessão — direciona para a landing page."""
    notice = f"<p style='color:{NEGATIVE}; font-weight:600'>{message}</p>" if message else ""
    st.markdown(
        '<div class="c5c-gate">'
        f'<div class="coin">🪙</div>'
        "<h1>Sua jornada começa lá na página inicial</h1>"
        + notice
        + "<p>Entre ou crie sua conta gratuita na página oficial do 5 Centavos. "
          "É rápido, seguro e grátis para sempre.</p>"
        f'<a class="c5c-btn" href="{landing_url}">Ir para a página inicial →</a>'
        '<p class="micro">Sem cartão de crédito · Leva 30 segundos</p>'
        "</div>",
        unsafe_allow_html=True,
    )
