"""Testes end-to-end: jornadas completas do usuário pela API."""

from datetime import date


def _register_and_login(client, email):
    client.post(
        "/api/v1/auth/register",
        json={"name": "E2E", "email": email, "password": "senha123"},
    )
    token = client.post(
        "/api/v1/auth/login", json={"email": email, "password": "senha123"}
    ).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


class TestJornadaCompleta:
    def test_cadastro_ate_insights_de_ia(self, client):
        """CU01→CU02→CU03→CU04/05→CU06→CU11→CU12→CU16: fluxo inteiro."""
        headers = _register_and_login(client, "jornada@example.com")

        # Conta
        account = client.post(
            "/api/v1/users/me/accounts",
            json={"name": "Banco", "type": "CORRENTE", "initial_balance": "2000"},
            headers=headers,
        ).json()

        categories = client.get("/api/v1/users/me/categories", headers=headers).json()
        receita = next(c for c in categories if c["type"] == "RECEITA")
        despesa = next(c for c in categories if c["name"] == "Alimentação")

        # Transações ao longo de 3 meses (base para IA — mínimo 8 registros)
        for month in (7, 8, 9, 10):
            for desc, amount, type_, cat in [
                (f"salario {month}", "5000", "RECEITA", receita),
                (f"mercado {month}", "800", "DESPESA", despesa),
            ]:
                response = client.post(
                    "/api/v1/transactions",
                    json={
                        "account_id": account["id"],
                        "category_id": cat["id"],
                        "description": desc,
                        "amount": amount,
                        "type": type_,
                        "date": date(2026, month, 10).isoformat(),
                    },
                    headers=headers,
                )
                assert response.status_code == 201

        # Saldo esperado: 2000 + 4*(5000 - 800) = 18800
        balance = client.get(
            f"/api/v1/users/me/accounts/{account['id']}", headers=headers
        ).json()["balance"]
        assert balance == "18800.00"

        # Indicadores
        summary = client.get("/api/v1/analytics/summary", headers=headers).json()
        assert summary["taxa_poupanca"] == 84.0

        monthly = client.get("/api/v1/analytics/monthly", headers=headers).json()
        assert len(monthly) == 4

        # Meta com progresso
        goal = client.post(
            "/api/v1/goals",
            json={"name": "E2E meta", "target_amount": "10000", "deadline": "2027-12-31"},
            headers=headers,
        ).json()
        progressed = client.post(
            f"/api/v1/goals/{goal['id']}/progress",
            json={"amount": "2500"},
            headers=headers,
        ).json()
        assert progressed["current_amount"] == "2500.00"

        # IA treina e gera insights com base nos dados reais
        train = client.post("/api/v1/ai/train", headers=headers).json()
        assert train["transactions_used"] == 8

        insights = client.get("/api/v1/ai/insights", headers=headers).json()
        assert insights["insights"]
        assert "sugestões" in insights["disclaimer"].lower()

        prediction = client.post(
            "/api/v1/ai/predict-category",
            json={"description": "mercado padaria", "amount": "100", "type": "DESPESA"},
            headers=headers,
        ).json()
        assert prediction["category_name"] == "Alimentação"


class TestIsolamentoPontaAPonta:
    def test_usuarios_nao_se_enxergam(self, client):
        """RNF02: isolamento total dos dados entre usuários."""
        headers_a = _register_and_login(client, "a@e2e.com")
        headers_b = _register_and_login(client, "b@e2e.com")

        account_b = client.post(
            "/api/v1/users/me/accounts",
            json={"name": "Privada B", "type": "POUPANCA", "initial_balance": "500"},
            headers=headers_b,
        ).json()

        # Usuário A não enxerga nem consegue operar a conta de B
        assert (
            client.get(f"/api/v1/users/me/accounts/{account_b['id']}", headers=headers_a).status_code
            == 404
        )
        assert client.get("/api/v1/users/me/accounts", headers=headers_a).json() == []
