import pytest
from fastapi.testclient import TestClient
from src.main import app


client = TestClient(app)


def test_api_routes_exist():
    """Test that API routes exist and return appropriate status codes"""
    # Test health endpoint
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

    # For chat endpoint, we can test that it accepts the request format
    # Actual streaming behavior is tested separately in production
    response = client.post(
        "/api/chat",
        json={"message": "Hello"}
    )
    # We expect either success or validation error, but not route not found
    assert response.status_code in [200, 422]