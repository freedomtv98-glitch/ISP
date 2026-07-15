"""Monitoring task scheduler."""

import asyncio
import logging
from typing import Callable, Dict, List

logger = logging.getLogger(__name__)


class MonitoringScheduler:
    """Manages periodic monitoring tasks."""

    def __init__(self):
        """Initialize scheduler."""
        self.tasks: Dict[str, asyncio.Task] = {}
        self.running = False

    async def add_task(
        self,
        name: str,
        coroutine: Callable,
        interval: int,
    ) -> None:
        """Add a periodic task to the scheduler.
        
        Args:
            name: Task name
            coroutine: Async function to run
            interval: Interval in seconds between runs
        """
        while self.running:
            try:
                await coroutine()
            except Exception as e:
                logger.error(f"Error in task {name}: {e}")
            
            await asyncio.sleep(interval)

    async def run(self) -> None:
        """Run the scheduler."""
        self.running = True
        logger.info("Monitoring scheduler started")
        
        try:
            while self.running:
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            logger.info("Monitoring scheduler stopped")
            self.running = False
