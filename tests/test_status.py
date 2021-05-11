"""
test_status.py
Tests the /status API endpoints
"""
import pytest
from app.config import get_settings


@pytest.mark.asyncio
def test_status_get(test_client, settings):
    """
    Tests /status [GET]
    :param test_client: Fast API test client fixture
    :param settings: Settings test fixture
    """
    with test_client as tc:
        settings.uvicorn_reload = False
        tc.app.dependency_overrides[get_settings] = lambda: settings
        actual_response = tc.get("/status")

        assert actual_response.status_code == 200

        actual_json = actual_response.json()
        assert "application_version" in actual_json

        expected = {
            "application": "app.asgi:app",
            "application_version": actual_json["application_version"],
            "is_reload_enabled": False,
        }
        assert actual_json == expected
