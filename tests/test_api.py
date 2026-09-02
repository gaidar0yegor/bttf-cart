"""Tests d'intégration de l'API HTTP (FastAPI).

L'API est un adaptateur mince : elle délègue au domaine et traduit
les erreurs en réponses HTTP explicites (422 pour un film inconnu,
toujours avec le détail du calcul quand le panier est valide).
"""

from bttf.api import app
from fastapi.testclient import TestClient


def test_api_returns_total_and_breakdown() -> None:
    # Given
    client = TestClient(app)
    payload = {"cart_text": "Back to the Future 1\nBack to the Future 2\nBack to the Future 3"}

    # When
    response = client.post("/api/price", json=payload)

    # Then
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 36
    assert body["breakdown"]["subtotal"] == 45
    assert body["breakdown"]["discount_percent"] == 20
    assert body["breakdown"]["discount_amount"] == 9
    assert body["breakdown"]["total"] == 36


def test_api_rejects_unknown_movie_with_422_and_message() -> None:
    # Given
    client = TestClient(app)

    # When
    response = client.post("/api/price", json={"cart_text": "Back to the Future 4"})

    # Then
    assert response.status_code == 422
    assert "film inconnu" in response.json()["detail"].lower()


def test_api_serves_the_web_page() -> None:
    # Given
    client = TestClient(app)

    # When
    response = client.get("/")

    # Then
    assert response.status_code == 200
    assert "Back to the Future" in response.text


def test_api_empty_cart_is_zero() -> None:
    # Given
    client = TestClient(app)

    # When
    response = client.post("/api/price", json={"cart_text": ""})

    # Then
    assert response.status_code == 200
    assert response.json()["total"] == 0
