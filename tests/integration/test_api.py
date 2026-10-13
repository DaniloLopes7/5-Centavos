"""Testes de integração da API REST (contratos HTTP completos)."""


class TestAuth:
    def test_register_login_me(self, client, auth_headers):
        response = client.post(
            "/api/v1/auth/register",
            json={"name": "Maria", "email": "maria@example.com", "password": "senha123"},
        )
        assert response.status_code == 201
        body = response.json()
        assert body["email"] == "maria@example.com"
        assert "password" not in body and "password_hash" not in body

        me = client.get("/api/v1/auth/me", headers=auth_headers)
        assert me.status_code == 200
        assert me.json()["email"] == "teste@example.com"

    def test_login_credenciais_invalidas(self, client, auth_headers):
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "teste@example.com", "password": "errada"},
        )
        assert response.status_code == 401

    def test_rotas_exigem_token(self, client):
        assert client.get("/api/v1/transactions").status_code == 401
        assert client.get("/api/v1/goals").status_code == 401
        assert client.get("/api/v1/analytics/summary").status_code == 401

    def test_token_invalido(self, client):
        response = client.get(
            "/api/v1/auth/me", headers={"Authorization": "Bearer lixo"}
        )
        assert response.status_code == 401


class TestAccounts:
    def test_crud_completo(self, client, auth_headers, account_id):
        listing = client.get("/api/v1/users/me/accounts", headers=auth_headers)
        assert listing.status_code == 200
        assert len(listing.json()) == 1
        assert listing.json()[0]["balance"] == "1000.00"

        updated = client.put(
            f"/api/v1/users/me/accounts/{account_id}",
            json={"name": "Conta Nova"},
            headers=auth_headers,
        )
        assert updated.status_code == 200
        assert updated.json()["name"] == "Conta Nova"

        deleted = client.delete(
            f"/api/v1/users/me/accounts/{account_id}", headers=auth_headers
        )
        assert deleted.status_code == 204

    def test_tipo_invalido_retorna_422(self, client, auth_headers):
        response = client.post(
            "/api/v1/users/me/accounts",
            json={"name": "X", "type": "INEXISTENTE", "initial_balance": "0"},
            headers=auth_headers,
        )
        assert response.status_code == 422


class TestCategories:
    def test_categorias_padrao_e_criacao(self, client, auth_headers):
        categories = client.get("/api/v1/users/me/categories", headers=auth_headers).json()
        assert len(categories) == 10

        created = client.post(
            "/api/v1/users/me/categories",
            json={"name": "Assinaturas", "type": "DESPESA"},
            headers=auth_headers,
        )
        assert created.status_code == 201

        duplicated = client.post(
            "/api/v1/users/me/categories",
            json={"name": "Assinaturas", "type": "DESPESA"},
            headers=auth_headers,
        )
        assert duplicated.status_code == 409


class TestTransactions:
    def test_ciclo_de_vida_com_saldo(self, client, auth_headers, account_id, category_ids):
        created = client.post(
            "/api/v1/transactions",
            json={
                "account_id": account_id,
                "category_id": category_ids["receita"],
                "description": "Salário",
                "amount": "2500.00",
                "type": "RECEITA",
                "date": "2026-10-01",
            },
            headers=auth_headers,
        )
        assert created.status_code == 201
        tx = created.json()

        listing = client.get("/api/v1/transactions", headers=auth_headers)
        assert len(listing.json()) == 1

        accounts = client.get("/api/v1/users/me/accounts", headers=auth_headers).json()
        assert accounts[0]["balance"] == "3500.00"

        updated = client.put(
            f"/api/v1/transactions/{tx['id']}", json={"amount": "2000"}, headers=auth_headers
        )
        assert updated.json()["amount"] == "2000.00"

        assert client.delete(
            f"/api/v1/transactions/{tx['id']}", headers=auth_headers
        ).status_code == 204
        accounts = client.get("/api/v1/users/me/accounts", headers=auth_headers).json()
        assert accounts[0]["balance"] == "1000.00"

    def test_valor_nao_positivo_rejeitado(self, client, auth_headers, account_id, category_ids):
        for amount in ("0", "-10"):
            response = client.post(
                "/api/v1/transactions",
                json={
                    "account_id": account_id,
                    "category_id": category_ids["receita"],
                    "description": "Inválido",
                    "amount": amount,
                    "type": "RECEITA",
                    "date": "2026-10-01",
                },
                headers=auth_headers,
            )
            assert response.status_code == 422

    def test_tipo_incompativel_categoria(self, client, auth_headers, account_id, category_ids):
        response = client.post(
            "/api/v1/transactions",
            json={
                "account_id": account_id,
                "category_id": category_ids["despesa"],
                "description": "Errado",
                "amount": "100",
                "type": "RECEITA",
                "date": "2026-10-01",
            },
            headers=auth_headers,
        )
        assert response.status_code == 422

    def test_isolamento_entre_usuarios(self, client, auth_headers, account_id, category_ids):
        tx = client.post(
            "/api/v1/transactions",
            json={
                "account_id": account_id,
                "category_id": category_ids["receita"],
                "description": "Privado",
                "amount": "100",
                "type": "RECEITA",
                "date": "2026-10-01",
            },
            headers=auth_headers,
        ).json()

        client.post(
            "/api/v1/auth/register",
            json={"name": "Intruso", "email": "intruso@example.com", "password": "senha123"},
        )
        token = client.post(
            "/api/v1/auth/login",
            json={"email": "intruso@example.com", "password": "senha123"},
        ).json()["access_token"]
        other_headers = {"Authorization": f"Bearer {token}"}

        assert client.get(f"/api/v1/transactions/{tx['id']}", headers=other_headers).status_code == 404
        assert client.get("/api/v1/transactions", headers=other_headers).json() == []


class TestGoals:
    def test_crud_e_progresso(self, client, auth_headers):
        created = client.post(
            "/api/v1/goals",
            json={"name": "Reserva", "target_amount": "5000", "deadline": "2027-01-01"},
            headers=auth_headers,
        )
        assert created.status_code == 201
        goal_id = created.json()["id"]

        response = client.post(
            f"/api/v1/goals/{goal_id}/progress", json={"amount": "500"}, headers=auth_headers
        )
        assert response.json()["current_amount"] == "500.00"

        deleted = client.delete(f"/api/v1/goals/{goal_id}", headers=auth_headers)
        assert deleted.status_code == 204


class TestAnalytics:
    def test_summary_monthly_categories(self, client, auth_headers, account_id, category_ids):
        client.post(
            "/api/v1/transactions",
            json={
                "account_id": account_id,
                "category_id": category_ids["receita"],
                "description": "Salário",
                "amount": "4000",
                "type": "RECEITA",
                "date": "2026-09-05",
            },
            headers=auth_headers,
        )
        client.post(
            "/api/v1/transactions",
            json={
                "account_id": account_id,
                "category_id": category_ids["despesa"],
                "description": "Aluguel",
                "amount": "1500",
                "type": "DESPESA",
                "date": "2026-09-10",
            },
            headers=auth_headers,
        )

        summary = client.get("/api/v1/analytics/summary", headers=auth_headers).json()
        assert summary["total_receitas"] == "4000.00"
        assert summary["total_despesas"] == "1500.00"
        assert summary["saldo_atual"] == "3500.00"
        assert summary["taxa_poupanca"] == 62.5

        monthly = client.get("/api/v1/analytics/monthly", headers=auth_headers).json()
        assert monthly[0]["year_month"] == "2026-09"

        categories = client.get("/api/v1/analytics/categories", headers=auth_headers).json()
        assert len(categories) == 2

    def test_filtro_por_periodo(self, client, auth_headers, account_id, category_ids):
        for day in ("2026-01-05", "2026-03-05"):
            client.post(
                "/api/v1/transactions",
                json={
                    "account_id": account_id,
                    "category_id": category_ids["receita"],
                    "description": "Salário",
                    "amount": "1000",
                    "type": "RECEITA",
                    "date": day,
                },
                headers=auth_headers,
            )
        filtered = client.get(
            "/api/v1/transactions",
            params={"start_date": "2026-02-01", "end_date": "2026-03-31"},
            headers=auth_headers,
        ).json()
        assert len(filtered) == 1


class TestIA:
    def test_endpoints_ai(self, client, auth_headers, account_id, category_ids):
        for i in range(10):
            client.post(
                "/api/v1/transactions",
                json={
                    "account_id": account_id,
                    "category_id": category_ids["despesa"],
                    "description": f"mercado compra {i}",
                    "amount": str(200 + i * 10),
                    "type": "DESPESA",
                    "date": "2026-{:02d}-10".format((i % 4) + 1),
                },
                headers=auth_headers,
            )

        assert client.post("/api/v1/ai/train", headers=auth_headers).status_code == 200

        prediction = client.post(
            "/api/v1/ai/predict-category",
            json={"description": "compra no mercado", "amount": "150", "type": "DESPESA"},
            headers=auth_headers,
        ).json()
        assert prediction["category_name"]

        insights = client.get("/api/v1/ai/insights", headers=auth_headers)
        assert insights.status_code == 200
        assert insights.json()["insights"]

        cashflow = client.get("/api/v1/ai/cashflow-prediction", headers=auth_headers)
        assert cashflow.status_code == 200

        anomalies = client.get("/api/v1/ai/anomalies", headers=auth_headers)
        assert anomalies.status_code == 200


class TestInfra:
    def test_health_e_root(self, client):
        assert client.get("/health").json()["status"] == "ok"
        assert "docs" in client.get("/").json()
