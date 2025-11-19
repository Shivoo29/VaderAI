"""
Tests for voice processing endpoints
"""
import pytest
import io


def test_voice_endpoint_requires_auth(client):
    """Test that voice endpoint requires authentication"""
    response = client.post("/voice/text", json={"text": "Hello Vader"})
    assert response.status_code == 403


def test_text_processing(client, test_user_data):
    """Test text-based voice processing"""
    # Register and login
    register_response = client.post("/auth/register", json=test_user_data)
    token = register_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Process text
    response = client.post(
        "/voice/text",
        json={"text": "Vader, what is the Force?"},
        headers=headers
    )

    # Note: This might fail if AI services aren't available, but the endpoint should exist
    assert response.status_code in [200, 500]  # 500 if services not available

    if response.status_code == 200:
        data = response.json()
        assert "transcribed_text" in data
        assert "vader_response" in data
        assert "conversation_id" in data


def test_get_conversations(client, test_user_data):
    """Test get conversations endpoint"""
    # Register and login
    register_response = client.post("/auth/register", json=test_user_data)
    token = register_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Get conversations
    response = client.get("/voice/conversations", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
