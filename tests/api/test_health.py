"""
Tests for API endpoints.
"""

from fastapi.testclient import TestClient

from app.main import app

HTTP_OK = 200


def test_health_check() -> None:
    """Test health check endpoint."""
    client = TestClient(app)
    response = client.get("/api/v1/health")
    assert response.status_code == HTTP_OK
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "dlrs-auth"
