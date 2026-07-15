"""Health check endpoints."""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str


@router.get("/", response_model=HealthResponse)
async def health_check():
    """Check system health."""
    return {
        "status": "healthy",
        "version": "1.0.0",
    }
