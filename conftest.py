"""Pytest configuration for the test suite."""
import pytest
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


@pytest.fixture
def api_base_url():
    """Provide the API base URL for tests."""
    return "http://localhost:8000"


@pytest.fixture
def sample_text():
    """Provide sample text for testing."""
    return """
    Artificial intelligence is revolutionizing multiple industries. 
    From healthcare diagnostics to autonomous vehicles, AI is creating new possibilities. 
    Machine learning algorithms process massive datasets to find patterns humans might miss.
    """


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
