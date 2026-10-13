"""Cliente HTTP da API do 5 Centavos usado pelo dashboard."""

from __future__ import annotations

import os
from typing import Any

import httpx

API_URL = os.getenv("API_URL", "http://localhost:8000")


class ApiError(Exception):
    """Erro devolvido pela API (detail mapeado)."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class ApiClient:
    """Encapsula chamadas autenticadas à API REST."""

    def __init__(self, token: str | None = None) -> None:
        self.token = token

    def _headers(self) -> dict[str, str]:
        base = {"Content-Type": "application/json"}
        if self.token:
            base["Authorization"] = f"Bearer {self.token}"
        return base

    def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        with httpx.Client(base_url=API_URL, timeout=30.0) as client:
            response = client.request(method, path, headers=self._headers(), **kwargs)
        if response.status_code == 204:
            return None
        payload = response.json() if response.content else None
        if response.status_code >= 400:
            detail = payload.get("detail") if isinstance(payload, dict) else payload
            raise ApiError(str(detail), response.status_code)
        return payload

    # Autenticação -------------------------------------------------------
    def login(self, email: str, password: str) -> str:
        payload = self._request("POST", "/api/v1/auth/login", json={"email": email, "password": password})
        return payload["access_token"]

    def register(self, name: str, email: str, password: str) -> None:
        self._request("POST", "/api/v1/auth/register", json={"name": name, "email": email, "password": password})

    def me(self) -> dict:
        return self._request("GET", "/api/v1/auth/me")

    # Genéricos ----------------------------------------------------------
    def list_(self, path: str, params: dict | None = None) -> Any:
        return self._request("GET", path, params=params)

    def create(self, path: str, data: dict) -> Any:
        return self._request("POST", path, json=data)

    def update(self, path: str, data: dict) -> Any:
        return self._request("PUT", path, json=data)

    def delete(self, path: str) -> None:
        self._request("DELETE", path)
