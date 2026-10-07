"""
Módulo de Inteligência Artificial para 5 Centavos

Funcionalidades:
- Classificação automática de transações
- Detecção de anomalias (gastos incomuns)
- Previsão de fluxo de caixa
- Sugestões de economia
- Clustering de padrões de gasto
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.cluster import KMeans
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import joblib
import warnings
warnings.filterwarnings('ignore')

from src.repositories import AnalyticsRepository, TransactionRepository


class TransactionClassifier:
    """Classificador automático de categorias para transações baseadas na descrição."""
    
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.vectorizer = None  # TF-IDF para texto
        self.label_encoder = LabelEncoder()
        self.is_trained = False
    
    def _extract_features(self, descriptions: List[str]) -> np.ndarray:
        """Extrai features simples das descrições."""
        # Features básicas: comprimento, presença de palavras-chave
        features = []
        keywords = {
            'alimentacao': ['supermercado', 'mercado', 'restaurante', 'lanche', 'comida', 'almoco', 'jantar', 'cafe', 'padaria'],
            'transporte': ['uber', '99', 'taxi', 'onibus', 'metro', 'combustivel', 'posto', 'estacionamento', 'pedagio'],
            'lazer': ['cinema', 'netflix', 'spotify', 'show', 'teatro', 'parque', 'jogo', 'bar', 'festa'],
            'saude': ['farmacia', 'medico', 'hospital', 'clinica', 'exame', 'remedio', 'dentista', 'psicologo'],
            'educacao': ['curso', 'livro', 'faculdade', 'escola', 'universidade', 'mensalidade', 'material'],
            'moradia': ['aluguel', 'condominio', 'energia', 'agua', 'internet', 'telefone', 'luz', 'gas'],
            'salario': ['salario', 'pagamento', 'folha', 'deposito', 'pix recebido', 'transferencia recebida'],
            'freelance': ['freelance', 'projeto', 'cliente', 'servico', 'consultoria', 'trabalho extra'],
        }
        
        for desc in descriptions:
            desc_lower = desc.lower()
            row = [len(desc)]
            for category, words in keywords.items():
                row.append(sum(1 for w in words if w in desc_lower))
            features.append(row)
        
        return np.array(features)
    
    def train(self, descriptions: List[str], categories: List[str]):
        """Treina o classificador."""
        X = self._extract_features(descriptions)
        y = self.label_encoder.fit_transform(categories)
        
        if len(np.unique(y)) < 2:
            return False
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_test)
        self.is_trained = True
        
        return True
    
    def predict(self, description: str) -> str:
        """Prediz a categoria para uma descrição."""
        if not self.is_trained:
            return "Outros"
        
        X = self._extract_features([description])
        pred = self.model.predict(X)
        return self.label_encoder.inverse_transform(pred)[0]
    
    def save(self, path: str):
        """Salva o modelo."""
        joblib.dump({
            'model': self.model,
            'label_encoder': self.label_encoder,
            'is_trained': self.is_trained
        }, path)
    
    def load(self, path: str):
        """Carrega o modelo."""
        data = joblib.load(path)
        self.model = data['model']
        self.label_encoder = data['label_encoder']
        self.is_trained = data['is_trained']


class AnomalyDetector:
    """Detector de anomalias em transações (gastos incomuns)."""
    
    def __init__(self, contamination: float = 0.1):
        self.model = IsolationForest(contamination=contamination, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def _prepare_data(self, transactions: List[dict]) -> np.ndarray:
        """Prepara dados para detecção de anomalias."""
        features = []
        for t in transactions:
            # Features: valor, hora do dia, dia da semana, tipo
            date = pd.to_datetime(t['date'])
            features.append([
                float(t['amount']),
                date.hour,
                date.weekday(),
                1 if t['type'] == 'DESPESA' else 0
            ])
        return np.array(features)
    
    def train(self, transactions: List[dict]):
        """Treina o detector de anomalias."""
        if len(transactions) < 10:
            return False
        
        X = self._prepare_data(transactions)
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled)
        self.is_trained = True
        return True
    
    def detect(self, transactions: List[dict]) -> List[bool]:
        """Detecta anomalias nas transações."""
        if not self.is_trained or len(transactions) == 0:
            return [False] * len(transactions)
        
        X = self._prepare_data(transactions)
        X_scaled = self.scaler.transform(X)
        predictions = self.model.predict(X_scaled)
        # -1 = anomalia, 1 = normal
        return [p == -1 for p in predictions]
    
    def get_anomaly_scores(self, transactions: List[dict]) -> List[float]:
        """Retorna scores de anomalia (mais negativo = mais anômalo)."""
        if not self.is_trained or len(transactions) == 0:
            return [0.0] * len(transactions)
        
        X = self._prepare_data(transactions)
        X_scaled = self.scaler.transform(X)
        return self.model.decision_function(X_scaled).tolist()


class CashFlowPredictor:
    """Preditor de fluxo de caixa futuro."""
    
    def __init__(self):
        self.revenue_model = None
        self.expense_model = None
        self.is_trained = False
    
    def _prepare_time_series(self, transactions: List[dict]) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Prepara séries temporais de receitas e despesas."""
        df = pd.DataFrame(transactions)
        if df.empty:
            return pd.DataFrame(), pd.DataFrame()
        
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.to_period('M')
        
        revenue = df[df['type'] == 'RECEITA'].groupby('month')['amount'].sum().reset_index()
        expense = df[df['type'] == 'DESPESA'].groupby('month')['amount'].sum().reset_index()
        
        return revenue, expense
    
    def train(self, transactions: List[dict]):
        """Treina modelos de previsão simples baseados em médias móveis."""
        revenue, expense = self._prepare_time_series(transactions)
        
        if len(revenue) >= 3 and len(expense) >= 3:
            self.is_trained = True
            # Guarda as médias móveis para previsão
            self.revenue_ma = revenue['amount'].rolling(3, min_periods=1).mean().iloc[-1]
            self.expense_ma = expense['amount'].rolling(3, min_periods=1).mean().iloc[-1]
            return True
        return False
    
    def predict_next_months(self, months: int = 3) -> List[Dict]:
        """Prediz fluxo de caixa para os próximos meses."""
        if not self.is_trained:
            return []
        
        predictions = []
        last_month = datetime.now().replace(day=1)
        
        for i in range(months):
            pred_month = last_month + timedelta(days=32 * (i + 1))
            pred_month = pred_month.replace(day=1)
            
            predictions.append({
                'month': pred_month.strftime('%Y-%m'),
                'predicted_revenue': round(self.revenue_ma, 2),
                'predicted_expense': round(self.expense_ma, 2),
                'predicted_balance': round(self.revenue_ma - self.expense_ma, 2)
            })
        
        return predictions


class SpendingClusterer:
    """Agrupamento de padrões de gasto usando K-Means."""
    
    def __init__(self, n_clusters: int = 3):
        self.n_clusters = n_clusters
        self.model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def _prepare_user_features(self, transactions: List[dict]) -> np.ndarray:
        """Prepara features por usuário para clustering."""
        df = pd.DataFrame(transactions)
        if df.empty:
            return np.array([])
        
        df['date'] = pd.to_datetime(df['date'])
        expenses = df[df['type'] == 'DESPESA']
        
        if expenses.empty:
            return np.array([])
        
        # Features por categoria
        cat_totals = expenses.groupby('category_id')['amount'].sum()
        total_expense = expenses['amount'].sum()
        
        # Percentual por categoria
        features = []
        for cat_id, amount in cat_totals.items():
            features.append(amount / total_expense if total_expense > 0 else 0)
        
        # Adicionar features agregadas
        features.extend([
            total_expense,
            expenses['amount'].mean(),
            expenses['amount'].std() if len(expenses) > 1 else 0,
            len(expenses)
        ])
        
        return np.array(features).reshape(1, -1)
    
    def train(self, all_user_transactions: Dict[int, List[dict]]):
        """Treina o clusterizador com dados de múltiplos usuários."""
        all_features = []
        for user_id, transactions in all_user_transactions.items():
            features = self._prepare_user_features(transactions)
            if len(features) > 0:
                all_features.append(features[0])
        
        if len(all_features) < self.n_clusters:
            return False
        
        X = np.array(all_features)
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled)
        self.is_trained = True
        return True
    
    def predict_user_profile(self, transactions: List[dict]) -> int:
        """Prediz o cluster/perfil de um usuário."""
        if not self.is_trained:
            return 0
        
        features = self._prepare_user_features(transactions)
        if len(features) == 0:
            return 0
        
        X_scaled = self.scaler.transform(features)
        return self.model.predict(X_scaled)[0]
    
    def get_cluster_insights(self, cluster_id: int) -> Dict:
        """Retorna insights sobre um cluster."""
        insights = {
            0: {
                'name': 'Conservador',
                'description': 'Gastos concentrados em essenciais, alta taxa de poupança',
                'tips': ['Mantenha o foco em investimentos', 'Considere diversificar investimentos']
            },
            1: {
                'name': 'Equilibrado',
                'description': 'Gastos bem distribuídos entre essenciais e lazer',
                'tips': ['Revise assinaturas mensais', 'Automatize investimentos']
            },
            2: {
                'name': 'Gastador',
                'description': 'Alto gasto com lazer e não-essenciais',
                'tips': ['Crie orçamento por categoria', 'Use regra 50/30/20', 'Revise gastos supérfluos']
            }
        }
        return insights.get(cluster_id, insights[0])


class FinancialAdvisor:
    """Conselheiro financeiro que combina todos os modelos de IA."""
    
    def __init__(self):
        self.classifier = TransactionClassifier()
        self.anomaly_detector = AnomalyDetector()
        self.cashflow_predictor = CashFlowPredictor()
        self.clusterer = SpendingClusterer()
    
    def train_all(self, user_id: int):
        """Treina todos os modelos com dados do usuário."""
        from src.cinco_centavos.database import execute_query
        
        # Buscar transações do usuário
        query = """
            SELECT t.*, c.name as category_name 
            FROM transactions t
            JOIN accounts a ON t.account_id = a.id
            LEFT JOIN categories c ON t.category_id = c.id
            WHERE a.user_id = :user_id
            ORDER BY t.date
        """
        transactions = execute_query(query, {"user_id": user_id}, fetch=True) or []
        
        if not transactions:
            return {"status": "error", "message": "Dados insuficientes para treinamento."}
        
        results = {}
        
        # Treinar classificador (se tiver categorias)
        desc_with_cat = [t for t in transactions if t.get('category_name')]
        if len(desc_with_cat) >= 10:
            descriptions = [t['description'] for t in desc_with_cat]
            categories = [t['category_name'] for t in desc_with_cat]
            success = self.classifier.train(descriptions, categories)
            results['classifier'] = "treinado" if success else "dados insuficientes"
        
        # Treinar detector de anomalias
        success = self.anomaly_detector.train(transactions)
        results['anomaly_detector'] = "treinado" if success else "dados insuficientes"
        
        # Treinar preditor de fluxo de caixa
        success = self.cashflow_predictor.train(transactions)
        results['cashflow_predictor'] = "treinado" if success else "dados insuficientes"
        
        return results
    
    def get_insights(self, user_id: int) -> Dict:
        """Gera insights financeiros personalizados."""
        from src.cinco_centavos.database import execute_query
        
        query = """
            SELECT t.*, c.name as category_name 
            FROM transactions t
            JOIN accounts a ON t.account_id = a.id
            LEFT JOIN categories c ON t.category_id = c.id
            WHERE a.user_id = :user_id
            ORDER BY t.date
        """
        transactions = execute_query(query, {"user_id": user_id}, fetch=True) or []
        
        if not transactions:
            return {"insights": [], "predictions": [], "anomalies": []}
        
        # Treinar modelos se necessário
        if not self.anomaly_detector.is_trained:
            self.anomaly_detector.train(transactions)
        
        if not self.cashflow_predictor.is_trained:
            self.cashflow_predictor.train(transactions)
        
        insights = []
        predictions = []
        anomalies = []
        
        # 1. Detectar anomalias recentes
        recent_transactions = transactions[-20:] if len(transactions) >= 20 else transactions
        anomaly_flags = self.anomaly_detector.detect(recent_transactions)
        anomaly_scores = self.anomaly_detector.get_anomaly_scores(recent_transactions)
        
        for i, (t, is_anomaly, score) in enumerate(zip(recent_transactions, anomaly_flags, anomaly_scores)):
            if is_anomaly:
                anomalies.append({
                    'description': t['description'],
                    'amount': float(t['amount']),
                    'date': t['date'],
                    'type': t['type'],
                    'anomaly_score': round(score, 3),
                    'reason': 'Valor muito diferente do padrão habitual'
                })
        
        # 2. Previsão de fluxo de caixa
        predictions = self.cashflow_predictor.predict_next_months(3)
        
        # 3. Insights baseados em padrões
        df = pd.DataFrame(transactions)
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
            expenses = df[df['type'] == 'DESPESA']
            revenue = df[df['type'] == 'RECEITA']
            
            if not expenses.empty:
                # Top categorias de gasto
                cat_expenses = expenses.groupby('category_name')['amount'].sum().sort_values(ascending=False)
                top_cat = cat_expenses.index[0] if len(cat_expenses) > 0 else None
                top_amount = cat_expenses.iloc[0] if len(cat_expenses) > 0 else 0
                
                if top_cat:
                    insights.append({
                        'type': 'top_spending',
                        'title': f'Maior gasto: {top_cat}',
                        'message': f'Você gastou R$ {top_amount:,.2f} com {top_cat}. Considere revisar se é essencial.',
                        'priority': 'high' if top_amount > 1000 else 'medium'
                    })
                
                # Gasto médio diário
                daily_avg = expenses.groupby(df['date'].dt.date)['amount'].sum().mean()
                insights.append({
                    'type': 'daily_average',
                    'title': 'Gasto médio diário',
                    'message': f'Sua média de gastos diários é R$ {daily_avg:,.2f}.',
                    'priority': 'info'
                })
                
                # Detecção de assinaturas (gastos recorrentes)
                recurring = expenses.groupby(['category_name', 'amount']).size().reset_index(name='count')
                recurring = recurring[recurring['count'] >= 3]
                if not recurring.empty:
                    for _, row in recurring.iterrows():
                        insights.append({
                            'type': 'subscription',
                            'title': f'Possível assinatura: {row["category_name"]}',
                            'message': f'Gasto de R$ {row["amount"]:,.2f} repetido {row["count"]} vezes. Verifique se é necessário.',
                            'priority': 'medium'
                        })
        
        return {
            'insights': insights,
            'predictions': predictions,
            'anomalies': anomalies[:5]  # Top 5 anomalias
        }


# Instância global do advisor
advisor = FinancialAdvisor()