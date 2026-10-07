import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
from decimal import Decimal
import os

# Configuração da página
st.set_page_config(
    page_title="5 Centavos - Dashboard Financeiro",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuração da API
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")

# Estilo customizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .sidebar-header {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.token = None
    
    def set_token(self, token: str):
        self.token = token
    
    def get_headers(self):
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}
    
    def request(self, method: str, endpoint: str, **kwargs):
        url = f"{self.base_url}{endpoint}"
        headers = self.get_headers()
        if "headers" in kwargs:
            headers.update(kwargs.pop("headers"))
        response = requests.request(method, url, headers=headers, **kwargs)
        return response
    
    def login(self, email: str, password: str):
        response = self.request("POST", "/auth/login", data={"username": email, "password": password})
        if response.status_code == 200:
            data = response.json()
            self.set_token(data["access_token"])
            return data
        return None
    
    def register(self, name: str, email: str, password: str):
        response = self.request("POST", "/auth/register", json={"name": name, "email": email, "password": password})
        if response.status_code == 201:
            data = response.json()
            self.set_token(data["access_token"])
            return data
        return None
    
    # Account endpoints
    def get_accounts(self):
        return self.request("GET", "/users/me/accounts")
    
    def create_account(self, name: str, type: str, initial_balance: float):
        return self.request("POST", "/users/me/accounts", json={"name": name, "type": type, "initial_balance": initial_balance})
    
    # Category endpoints
    def get_categories(self):
        return self.request("GET", "/users/me/categories")
    
    def create_category(self, name: str, type: str):
        return self.request("POST", "/users/me/categories", json={"name": name, "type": type})
    
    # Transaction endpoints
    def get_transactions(self, account_id: int = None):
        params = {"account_id": account_id} if account_id else {}
        return self.request("GET", "/transactions", params=params)
    
    def create_transaction(self, account_id: int, category_id: int, description: str, amount: float, type: str, date: str):
        return self.request("POST", "/transactions", json={
            "account_id": account_id,
            "category_id": category_id,
            "description": description,
            "amount": amount,
            "type": type,
            "date": date
        })
    
    # Goal endpoints
    def get_goals(self):
        return self.request("GET", "/goals")
    
    def create_goal(self, name: str, target_amount: float, deadline: str = None):
        data = {"name": name, "target_amount": target_amount}
        if deadline:
            data["deadline"] = deadline
        return self.request("POST", "/goals", json=data)
    
    def add_goal_progress(self, goal_id: int, amount: float):
        return self.request("POST", f"/goals/{goal_id}/progress", json={"amount": amount})
    
    # Analytics endpoints
    def get_summary(self):
        return self.request("GET", "/analytics/summary")
    
    def get_category_summary(self):
        return self.request("GET", "/analytics/categories")
    
    def get_monthly_summary(self):
        return self.request("GET", "/analytics/monthly")


@st.cache_resource
def get_api_client():
    return APIClient(API_BASE_URL)


def login_page(api: APIClient):
    st.markdown('<h1 class="main-header">💰 5 Centavos</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666;">Sua plataforma de gestão financeira pessoal</p>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Cadastro"])
    
    with tab1:
        with st.form("login_form"):
            email = st.text_input("E-mail", placeholder="seu@email.com")
            password = st.text_input("Senha", type="password", placeholder="********")
            submit = st.form_submit_button("Entrar", use_container_width=True)
            
            if submit:
                if email and password:
                    result = api.login(email, password)
                    if result:
                        st.success("Login realizado com sucesso!")
                        st.rerun()
                    else:
                        st.error("E-mail ou senha incorretos.")
                else:
                    st.error("Preencha todos os campos.")
    
    with tab2:
        with st.form("register_form"):
            name = st.text_input("Nome completo", placeholder="João Silva")
            email = st.text_input("E-mail", placeholder="seu@email.com")
            password = st.text_input("Senha", type="password", placeholder="********")
            confirm = st.text_input("Confirmar senha", type="password", placeholder="********")
            submit = st.form_submit_button("Cadastrar", use_container_width=True)
            
            if submit:
                if name and email and password and confirm:
                    if password != confirm:
                        st.error("As senhas não coincidem.")
                    elif len(password) < 6:
                        st.error("A senha deve ter pelo menos 6 caracteres.")
                    else:
                        result = api.register(name, email, password)
                        if result:
                            st.success("Conta criada com sucesso!")
                            st.rerun()
                        else:
                            st.error("Erro ao criar conta. O e-mail pode já estar em uso.")
                else:
                    st.error("Preencha todos os campos.")


def sidebar_navigation(api: APIClient):
    with st.sidebar:
        st.markdown('<div class="sidebar-header">📊 5 Centavos</div>', unsafe_allow_html=True)
        
        if api.token:
            st.success("✅ Logado")
            if st.button("🚪 Sair", use_container_width=True):
                api.token = None
                st.rerun()
            
            st.divider()
            
            page = st.radio(
                "Navegação",
                ["📈 Dashboard", "🏦 Contas", "💳 Transações", "🏷️ Categorias", "🎯 Metas", "📊 Analytics"],
                key="navigation"
            )
            
            st.divider()
            st.caption("v0.7.0 - Dashboard")
            
            return page
        else:
            st.info("Faça login para acessar o dashboard.")
            return None


def dashboard_page(api: APIClient):
    st.header("📈 Dashboard")
    
    # Resumo financeiro
    summary_response = api.get_summary()
    if summary_response and summary_response.status_code == 200:
        summary = summary_response.json()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "💰 Receitas Totais",
                f"R$ {summary['total_revenue']:,.2f}",
                delta=None
            )
        
        with col2:
            st.metric(
                "💸 Despesas Totais",
                f"R$ {summary['total_expense']:,.2f}",
                delta=None
            )
        
        with col3:
            balance = summary['balance']
            st.metric(
                "💵 Saldo Total",
                f"R$ {balance:,.2f}",
                delta=f"{'Positivo' if balance >= 0 else 'Negativo'}",
                delta_color="normal" if balance >= 0 else "inverse"
            )
        
        with col4:
            st.metric(
                "📊 Transações",
                f"{summary['transactions_count']}",
                delta=None
            )
    else:
        st.warning("Não foi possível carregar o resumo financeiro.")
    
    st.divider()
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Gastos por Categoria")
        cat_response = api.get_category_summary()
        if cat_response and cat_response.status_code == 200:
            categories = cat_response.json()
            if categories:
                df_cat = pd.DataFrame(categories)
                df_cat = df_cat[df_cat['category_type'] == 'DESPESA']
                if not df_cat.empty:
                    fig = px.pie(
                        df_cat,
                        values='total_amount',
                        names='category_name',
                        title="Distribuição de Despesas"
                    )
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Nenhuma despesa registrada.")
            else:
                st.info("Nenhuma categoria encontrada.")
        else:
            st.info("Carregando dados...")
    
    with col2:
        st.subheader("📅 Evolução Mensal")
        monthly_response = api.get_monthly_summary()
        if monthly_response and monthly_response.status_code == 200:
            months = monthly_response.json()
            if months:
                df_monthly = pd.DataFrame(months)
                df_monthly['month'] = pd.to_datetime(df_monthly['month'] + '-01')
                df_monthly = df_monthly.sort_values('month')
                
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=df_monthly['month'],
                    y=df_monthly['revenue'],
                    name='Receitas',
                    marker_color='#2ecc71'
                ))
                fig.add_trace(go.Bar(
                    x=df_monthly['month'],
                    y=df_monthly['expense'],
                    name='Despesas',
                    marker_color='#e74c3c'
                ))
                fig.add_trace(go.Scatter(
                    x=df_monthly['month'],
                    y=df_monthly['balance'],
                    name='Saldo',
                    mode='lines+markers',
                    line=dict(color='#3498db', width=3)
                ))
                
                fig.update_layout(
                    title="Receitas vs Despesas por Mês",
                    barmode='group',
                    xaxis_title="Mês",
                    yaxis_title="Valor (R$)",
                    hovermode='x unified'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Nenhum dado mensal disponível.")
        else:
            st.info("Carregando dados...")


def accounts_page(api: APIClient):
    st.header("🏦 Minhas Contas")
    
    # Criar nova conta
    with st.expander("➕ Nova Conta", expanded=False):
        with st.form("new_account"):
            name = st.text_input("Nome da conta", placeholder="Ex: Nubank, Carteira, Poupança")
            type = st.selectbox("Tipo", ["Corrente", "Poupança", "Investimento", "Espécie", "Cartão de Crédito", "Outro"])
            initial_balance = st.number_input("Saldo inicial", min_value=0.0, format="%.2f")
            submit = st.form_submit_button("Criar conta")
            
            if submit:
                if name:
                    result = api.create_account(name, type, initial_balance)
                    if result and result.status_code == 201:
                        st.success("Conta criada com sucesso!")
                        st.rerun()
                    else:
                        st.error("Erro ao criar conta.")
                else:
                    st.error("Preencha o nome da conta.")
    
    # Listar contas
    accounts_response = api.get_accounts()
    if accounts_response and accounts_response.status_code == 200:
        accounts = accounts_response.json()
        
        if accounts:
            for acc in accounts:
                with st.container():
                    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                    with col1:
                        st.write(f"**{acc['name']}**")
                        st.caption(f"Tipo: {acc['type']}")
                    with col2:
                        balance = acc.get('current_balance', 0)
                        color = "green" if balance >= 0 else "red"
                        st.markdown(f"<h4 style='color: {color};'>R$ {balance:,.2f}</h4>", unsafe_allow_html=True)
                    with col3:
                        st.caption(f"Saldo inicial: R$ {acc['initial_balance']:,.2f}")
                    with col4:
                        if st.button("🗑️", key=f"del_acc_{acc['id']}", help="Excluir conta"):
                            # TODO: implement delete
                            pass
                    st.divider()
        else:
            st.info("Você não possui contas cadastradas. Crie sua primeira conta acima!")


def transactions_page(api: APIClient):
    st.header("💳 Transações")
    
    # Obter contas e categorias para os selects
    accounts_response = api.get_accounts()
    categories_response = api.get_categories()
    
    accounts = accounts_response.json() if accounts_response and accounts_response.status_code == 200 else []
    categories = categories_response.json() if categories_response and categories_response.status_code == 200 else []
    
    if not accounts:
        st.warning("Você precisa criar uma conta primeiro.")
        return
    
    if not categories:
        st.warning("Você precisa criar uma categoria primeiro.")
        return
    
    # Nova transação
    with st.expander("➕ Nova Transação", expanded=True):
        with st.form("new_transaction"):
            col1, col2 = st.columns(2)
            with col1:
                account = st.selectbox(
                    "Conta",
                    options=accounts,
                    format_func=lambda x: f"{x['name']} ({x['type']})"
                )
                category = st.selectbox(
                    "Categoria",
                    options=categories,
                    format_func=lambda x: f"{x['name']} ({x['type']})"
                )
            with col2:
                trans_type = st.radio("Tipo", ["RECEITA", "DESPESA"], horizontal=True)
                amount = st.number_input("Valor", min_value=0.01, format="%.2f")
            
            description = st.text_input("Descrição", placeholder="Ex: Supermercado, Salário, Uber...")
            date = st.date_input("Data", value=date.today())
            
            submit = st.form_submit_button("Registrar", use_container_width=True)
            
            if submit:
                if account and category and description and amount > 0:
                    # Filtrar categoria pelo tipo
                    cat = next((c for c in categories if c['id'] == category['id']), None)
                    if cat and cat['type'] != trans_type:
                        st.error(f"Categoria '{cat['name']}' é do tipo {cat['type']}, não {trans_type}.")
                    else:
                        result = api.create_transaction(
                            account['id'],
                            category['id'],
                            description,
                            amount,
                            trans_type,
                            date.strftime("%Y-%m-%d")
                        )
                        if result and result.status_code == 201:
                            st.success("Transação registrada com sucesso!")
                            st.rerun()
                        else:
                            st.error(f"Erro ao registrar: {result.text if result else 'Erro desconhecido'}")
                else:
                    st.error("Preencha todos os campos.")
    
    # Listar transações
    st.divider()
    st.subheader("📋 Extrato")
    
    account_filter = st.selectbox(
        "Filtrar por conta",
        options=[None] + accounts,
        format_func=lambda x: "Todas as contas" if x is None else f"{x['name']} ({x['type']})"
    )
    
    transactions_response = api.get_transactions(account_filter['id'] if account_filter else None)
    if transactions_response and transactions_response.status_code == 200:
        transactions = transactions_response.json()
        
        if transactions:
            df = pd.DataFrame(transactions)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date', ascending=False)
            
            # Formatação para exibição
            df_display = df.copy()
            df_display['Valor'] = df_display.apply(
                lambda row: f"+ R$ {row['amount']:,.2f}" if row['type'] == 'RECEITA' else f"- R$ {row['amount']:,.2f}",
                axis=1
            )
            df_display['Data'] = df_display['date'].dt.strftime('%d/%m/%Y')
            
            st.dataframe(
                df_display[['Data', 'description', 'Valor', 'type']].rename(columns={
                    'description': 'Descrição',
                    'type': 'Tipo'
                }),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Nenhuma transação encontrada.")
    else:
        st.error("Erro ao carregar transações.")


def categories_page(api: APIClient):
    st.header("🏷️ Categorias")
    
    # Nova categoria
    with st.expander("➕ Nova Categoria", expanded=False):
        with st.form("new_category"):
            name = st.text_input("Nome", placeholder="Ex: Alimentação, Transporte, Salário")
            type = st.radio("Tipo", ["RECEITA", "DESPESA"], horizontal=True)
            submit = st.form_submit_button("Criar")
            
            if submit:
                if name:
                    result = api.create_category(name, type)
                    if result and result.status_code == 201:
                        st.success("Categoria criada!")
                        st.rerun()
                    else:
                        st.error("Erro ao criar categoria.")
                else:
                    st.error("Preencha o nome.")
    
    # Listar categorias
    categories_response = api.get_categories()
    if categories_response and categories_response.status_code == 200:
        categories = categories_response.json()
        
        if categories:
            # Separar por tipo
            receitas = [c for c in categories if c['type'] == 'RECEITA']
            despesas = [c for c in categories if c['type'] == 'DESPESA']
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("💰 Receitas")
                for cat in receitas:
                    st.write(f"✅ {cat['name']}")
            
            with col2:
                st.subheader("💸 Despesas")
                for cat in despesas:
                    st.write(f"🔴 {cat['name']}")
        else:
            st.info("Nenhuma categoria cadastrada.")


def goals_page(api: APIClient):
    st.header("🎯 Metas Financeiras")
    
    # Nova meta
    with st.expander("➕ Nova Meta", expanded=False):
        with st.form("new_goal"):
            name = st.text_input("Nome da meta", placeholder="Ex: Reserva de emergência, Viagem, Carro")
            target = st.number_input("Valor alvo (R$)", min_value=0.01, format="%.2f")
            deadline = st.date_input("Prazo (opcional)", value=None)
            submit = st.form_submit_button("Criar meta")
            
            if submit:
                if name and target > 0:
                    deadline_str = deadline.strftime("%Y-%m-%d") if deadline else None
                    result = api.create_goal(name, target, deadline_str)
                    if result and result.status_code == 201:
                        st.success("Meta criada!")
                        st.rerun()
                    else:
                        st.error("Erro ao criar meta.")
                else:
                    st.error("Preencha todos os campos.")
    
    # Listar metas
    goals_response = api.get_goals()
    if goals_response and goals_response.status_code == 200:
        goals = goals_response.json()
        
        if goals:
            for goal in goals:
                with st.container():
                    progress = goal.get('progress_percentage', 0)
                    current = goal['current_amount']
                    target = goal['target_amount']
                    
                    st.subheader(f"🎯 {goal['name']}")
                    
                    col1, col2, col3 = st.columns([3, 2, 1])
                    with col1:
                        st.progress(min(progress / 100, 1.0))
                        st.caption(f"R$ {current:,.2f} de R$ {target:,.2f} ({progress:.1f}%)")
                    with col2:
                        if goal.get('deadline'):
                            deadline = datetime.strptime(goal['deadline'], "%Y-%m-%d").date()
                            days_left = (deadline - date.today()).days
                            if days_left > 0:
                                st.caption(f"⏰ {days_left} dias restantes")
                            elif days_left == 0:
                                st.caption("⏰ Prazo hoje!")
                            else:
                                st.caption(f"⚠️ {abs(days_left)} dias atrasado")
                    with col3:
                        # Adicionar progresso
                        with st.form(f"add_progress_{goal['id']}"):
                            amount = st.number_input("Valor", min_value=0.01, format="%.2f", key=f"amt_{goal['id']}")
                            if st.form_submit_button("Adicionar"):
                                result = api.add_goal_progress(goal['id'], amount)
                                if result and result.status_code == 200:
                                    st.success("Progresso atualizado!")
                                    st.rerun()
                                else:
                                    st.error("Erro ao atualizar.")
                    
                    st.divider()
        else:
            st.info("Nenhuma meta cadastrada. Crie sua primeira meta acima!")


def analytics_page(api: APIClient):
    st.header("📊 Analytics Avançado")
    
    # Resumo detalhado
    summary_response = api.get_summary()
    if summary_response and summary_response.status_code == 200:
        summary = summary_response.json()
        
        st.subheader("📈 Resumo Geral")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Receitas", f"R$ {summary['total_revenue']:,.2f}")
        with col2:
            st.metric("Despesas", f"R$ {summary['total_expense']:,.2f}")
        with col3:
            st.metric("Saldo", f"R$ {summary['balance']:,.2f}")
        with col4:
            savings_rate = (summary['balance'] / summary['total_revenue'] * 100) if summary['total_revenue'] > 0 else 0
            st.metric("Taxa de Poupança", f"{savings_rate:.1f}%")
    
    st.divider()
    
    # Gráfico de categorias detalhado
    st.subheader("📊 Análise por Categoria")
    cat_response = api.get_category_summary()
    if cat_response and cat_response.status_code == 200:
        categories = cat_response.json()
        if categories:
            df_cat = pd.DataFrame(categories)
            
            # Separar receitas e despesas
            df_rev = df_cat[df_cat['category_type'] == 'RECEITA']
            df_exp = df_cat[df_cat['category_type'] == 'DESPESA']
            
            col1, col2 = st.columns(2)
            
            with col1:
                if not df_rev.empty:
                    fig = px.bar(
                        df_rev,
                        x='total_amount',
                        y='category_name',
                        orientation='h',
                        title="Receitas por Categoria",
                        color='total_amount',
                        color_continuous_scale='Greens'
                    )
                    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                if not df_exp.empty:
                    fig = px.bar(
                        df_exp,
                        x='total_amount',
                        y='category_name',
                        orientation='h',
                        title="Despesas por Categoria",
                        color='total_amount',
                        color_continuous_scale='Reds'
                    )
                    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
                    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Tendência mensal
    st.subheader("📅 Tendência Mensal")
    monthly_response = api.get_monthly_summary()
    if monthly_response and monthly_response.status_code == 200:
        months = monthly_response.json()
        if months:
            df_monthly = pd.DataFrame(months)
            df_monthly['month'] = pd.to_datetime(df_monthly['month'] + '-01')
            df_monthly = df_monthly.sort_values('month')
            
            # Calcular médias móveis
            df_monthly['revenue_ma3'] = df_monthly['revenue'].rolling(3).mean()
            df_monthly['expense_ma3'] = df_monthly['expense'].rolling(3).mean()
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=df_monthly['month'],
                y=df_monthly['revenue'],
                name='Receitas',
                mode='lines+markers',
                line=dict(color='#2ecc71', width=2)
            ))
            
            fig.add_trace(go.Scatter(
                x=df_monthly['month'],
                y=df_monthly['expense'],
                name='Despesas',
                mode='lines+markers',
                line=dict(color='#e74c3c', width=2)
            ))
            
            fig.add_trace(go.Scatter(
                x=df_monthly['month'],
                y=df_monthly['balance'],
                name='Saldo',
                mode='lines+markers',
                line=dict(color='#3498db', width=3, dash='dot')
            ))
            
            fig.update_layout(
                title="Evolução Financeira Mensal",
                xaxis_title="Mês",
                yaxis_title="Valor (R$)",
                hovermode='x unified',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            st.plotly_chart(fig, use_container_width=True)


def main():
    api = get_api_client()
    
    # Verificar se está logado
    if not api.token:
        login_page(api)
        return
    
    # Sidebar
    page = sidebar_navigation(api)
    
    if not page:
        return
    
    # Roteamento de páginas
    if page == "📈 Dashboard":
        dashboard_page(api)
    elif page == "🏦 Contas":
        accounts_page(api)
    elif page == "💳 Transações":
        transactions_page(api)
    elif page == "🏷️ Categorias":
        categories_page(api)
    elif page == "🎯 Metas":
        goals_page(api)
    elif page == "📊 Analytics":
        analytics_page(api)


if __name__ == "__main__":
    main()