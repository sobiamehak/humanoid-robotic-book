import pytest
from fastapi.testclient import TestClient
from src.main import app


client = TestClient(app)


def test_health_endpoint():
    """Test the health endpoint returns correct status"""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}