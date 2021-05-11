"""
conftest.py

Global PyTest fixtures
"""
import pytest
from app.config import Settings
from httpx import AsyncClient
from app.main import get_app
from fastapi.testclient import TestClient


@pytest.fixture
def settings() -> Settings:
    """
    :return: Application Settings
    """
    settings_fields = {
        "uvicorn_app": "app.asgi:app",
        "uvicorn_reload": False,
        "app_cert_key_name": "./test.key",
        "app_cert_name": "./test.pem",
    }
    return Settings(**settings_fields)


@pytest.fixture
def test_client() -> TestClient:
    """
    Creates a Fast API Test Client for API testing
    :return: Fast API test client
    """
    return TestClient(get_app())


@pytest.fixture
def async_test_client() -> AsyncClient:
    """
    Creates an HTTPX AsyncClient for async API testing
    :return: HTTPX async test client
    """
    return AsyncClient(app=get_app(), base_url="http://testserver")
