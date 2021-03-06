"""
config.py
Defines application settings and configurations using Pydantic BaseSettings.
Settings may be overriden using environment variables.
Example:
    override uvicorn_port default setting
    export UVICORN_PORT=5050
    or
    UVICORN_PORT=5050 python {{ template }}/main.py
"""
from pydantic import BaseSettings
import os
from os.path import dirname, abspath
from functools import lru_cache
import certifi
import ssl


class Settings(BaseSettings):
    """
    Application Settings
    """

    # uvicorn settings
    uvicorn_app: str = "app.asgi:app"
    uvicorn_host: str = "0.0.0.0"
    uvicorn_port: int = 5000
    uvicorn_reload: bool = False

    # general certificate settings
    # path to "standard" CA certificates
    certificate_authority_path: str = certifi.where()
    certificate_verify: bool = False

    # {{ app }} settings
    app_ca_file: str = certifi.where()
    app_ca_path: str = None
    app_cert_name: str = "app-server.pem"
    app_cert_key_name: str = "app-server.key"
    app_config_directory: str = "/home/appuser/config"
    app_logging_config_path: str = "logging.yaml"
    app_rate_limit: str = "5/second"

    class Config:
        case_sensitive = False
        env_file = os.path.join(dirname(dirname(abspath(__file__))), ".env")


@lru_cache()
def get_settings() -> Settings:
    """Returns the settings instance"""
    return Settings()


@lru_cache()
def get_ssl_context(ssl_purpose: ssl.Purpose) -> ssl.SSLContext:
    """
    Returns a SSL Context configured for server auth with the certificate path
    :param ssl_purpose: Indicates if the context is used for server or client auth
    """
    settings = get_settings()
    ssl_context = ssl.create_default_context(ssl_purpose)
    ssl_context.load_verify_locations(
        cafile=settings.app_ca_file, capath=settings.app_ca_path
    )
    return ssl_context
