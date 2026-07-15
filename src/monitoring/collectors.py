"""Data collectors for various metrics."""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any

import psutil

logger = logging.getLogger(__name__)


class MetricCollector(ABC):
    """Base class for metric collectors."""

    @abstractmethod
    async def collect(self) -> Dict[str, Any]:
        """Collect metrics."""
        pass


class SystemMetricsCollector(MetricCollector):
    """Collects system-level metrics."""

    async def collect(self) -> Dict[str, Any]:
        """Collect CPU, memory, disk metrics."""
        return {
            "cpu_usage": psutil.cpu_percent(interval=1),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "process_count": len(psutil.pids()),
        }


class NetworkMetricsCollector(MetricCollector):
    """Collects network-level metrics."""

    async def collect(self) -> Dict[str, Any]:
        """Collect network statistics."""
        net_io = psutil.net_io_counters(pernic=True)
        
        metrics = {}
        for interface, stats in net_io.items():
            metrics[f"network_{interface}"] = {
                "bytes_sent": stats.bytes_sent,
                "bytes_recv": stats.bytes_recv,
                "packets_sent": stats.packets_sent,
                "packets_recv": stats.packets_recv,
                "errin": stats.errin,
                "errout": stats.errout,
                "dropin": stats.dropin,
                "dropout": stats.dropout,
            }
        
        return metrics
