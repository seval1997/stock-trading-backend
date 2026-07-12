import pytest
from backend.app import app


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    """Test the /api/health endpoint returns correct JSON"""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
    assert data["message"] == "Backend is alive"
