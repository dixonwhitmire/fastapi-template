"""
status.py

Implements the system /status API endpoint
"""
from fastapi import Depends
from fastapi.routing import APIRouter
from pydantic.main import BaseModel
from app import __version__
from app.config import get_settings

router = APIRouter()


class StatusResponse(BaseModel):
    """
    Status check response model.
    The response provides component specific and overall status information
    """

    application: str
    application_version: str
    is_reload_enabled: bool

    class Config:
        schema_extra = {
            "example": {"application": "app.main:app", "application_version": "0.25.0"}
        }


@router.get("", response_model=StatusResponse)
def get_status(settings=Depends(get_settings)):
    """
    :return: the current system status
    """
    status_fields = {
        "application": settings.uvicorn_app,
        "application_version": __version__,
        "is_reload_enabled": settings.uvicorn_reload,
    }
    return StatusResponse(**status_fields)
