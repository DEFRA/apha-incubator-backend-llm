"""Test suite for the summarisation API."""
import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.main import app
from src.models import SummariseRequest


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_get_config(client):
    """Test the configuration endpoint."""
    response = client.get("/config")
    assert response.status_code == 200
    data = response.json()
    assert "region" in data
    assert "model_id" in data


def test_summarise_request_model():
    """Test the SummariseRequest model."""
    # Valid request
    request = SummariseRequest(text="This is a test text to summarise.", max_length=50)
    assert request.text == "This is a test text to summarise."
    assert request.max_length == 50

    # Default max_length
    request = SummariseRequest(text="Test text")
    assert request.max_length == 100


def test_summarise_request_validation():
    """Test SummariseRequest validation."""
    # Empty text should fail
    with pytest.raises(ValueError):
        SummariseRequest(text="")

    # max_length too small should fail
    with pytest.raises(ValueError):
        SummariseRequest(text="Test", max_length=10)

    # max_length too large should fail
    with pytest.raises(ValueError):
        SummariseRequest(text="Test", max_length=2000)


def test_summarise_endpoint_with_mock(client, monkeypatch):
    """Test the summarise endpoint with mocked Bedrock response."""

    def mock_summarise(self, text, max_length, model_id=None):
        """Mock Bedrock summariser."""
        return {
            "summary": "This is a mock summary of the provided text.",
            "input_tokens": 50,
            "output_tokens": 20,
            "model": "anthropic.claude-3-sonnet-20240229-v1:0",
        }

    # Patch the summariser
    from src.bedrock_summarizer import BedrockSummariser

    monkeypatch.setattr(BedrockSummariser, "summarise", mock_summarise)

    # Test the endpoint
    payload = {
        "text": "This is a test text with multiple sentences that needs to be summarised.",
        "max_length": 50,
    }

    response = client.post("/summarise", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert data["summary"] == "This is a mock summary of the provided text."
    assert data["input_tokens"] == 50
    assert data["output_tokens"] == 20


def test_summarise_endpoint_missing_text(client):
    """Test the summarise endpoint with missing text."""
    payload = {"max_length": 50}

    response = client.post("/summarise", json=payload)
    assert response.status_code == 422  # Validation error


def test_summarise_endpoint_invalid_max_length(client):
    """Test the summarise endpoint with invalid max_length."""
    payload = {"text": "Test text", "max_length": 10}

    response = client.post("/summarise", json=payload)
    assert response.status_code == 422  # Validation error
