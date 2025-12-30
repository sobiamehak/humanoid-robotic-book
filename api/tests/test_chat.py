import pytest
from fastapi.testclient import TestClient
from src.main import app


client = TestClient(app)


def test_chat_endpoint_basic():
    """Test the chat endpoint returns correct response"""
    # Test basic chat functionality
    response = client.post(
        "/api/chat",
        json={"message": "Hello, world!"}
    )
    assert response.status_code == 200
    # Note: For SSE streaming, we're testing that the endpoint accepts the request
    # The actual streaming content would be tested differently in a real implementation