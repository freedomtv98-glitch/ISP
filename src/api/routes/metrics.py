"""Metrics endpoints."""

from typing import List, Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel

router = APIRouter()


class MetricPoint(BaseModel):
    """Single metric data point."""
    timestamp: str
    value: float
    unit: str


class MetricResponse(BaseModel):
    """Metric response."""
    name: str
    points: List[MetricPoint]


@router.get("/cpu", response_model=MetricResponse)
async def get_cpu_metrics(limit: Optional[int] = Query(100, ge=1, le=1000)):
    """Get CPU usage metrics."""
    return {
        "name": "cpu_usage",
        "points": [
            {
                "timestamp": "2024-01-01T00:00:00Z",
                "value": 45.5,
                "unit": "%",
            }
        ],
    }


@router.get("/memory", response_model=MetricResponse)
async def get_memory_metrics(limit: Optional[int] = Query(100, ge=1, le=1000)):
    """Get memory usage metrics."""
    return {
        "name": "memory_usage",
        "points": [
            {
                "timestamp": "2024-01-01T00:00:00Z",
                "value": 62.3,
                "unit": "%",
            }
        ],
    }


@router.get("/network", response_model=MetricResponse)
async def get_network_metrics(interface: Optional[str] = "eth0"):
    """Get network metrics for interface."""
    return {
        "name": "network_usage",
        "points": [
            {
                "timestamp": "2024-01-01T00:00:00Z",
                "value": 125.4,
                "unit": "Mbps",
            }
        ],
    }
