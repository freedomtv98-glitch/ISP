"""System information endpoints."""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class SystemInfo(BaseModel):
    """System information."""
    hostname: str
    uptime: float
    load_average: tuple
    cpu_count: int
    total_memory: int


@router.get("/info", response_model=SystemInfo)
async def get_system_info():
    """Get system information."""
    return {
        "hostname": "monitor-01",
        "uptime": 86400.0,
        "load_average": (0.5, 0.3, 0.2),
        "cpu_count": 8,
        "total_memory": 16000000000,
    }
