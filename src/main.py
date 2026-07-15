"""Main entry point for ISP monitoring system."""

import asyncio
import logging
from pathlib import Path

import uvicorn
from dotenv import load_dotenv

from src.app import create_app
from src.config import settings
from src.monitoring.scheduler import MonitoringScheduler

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=settings.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Start the monitoring system."""
    logger.info("Starting ISP Network Monitoring System")
    logger.info(f"Configuration: {settings.environment}")
    
    # Create FastAPI application
    app = create_app()
    
    # Initialize monitoring scheduler
    scheduler = MonitoringScheduler()
    
    # Start scheduler in background
    scheduler_task = asyncio.create_task(scheduler.run())
    
    # Run API server
    config = uvicorn.Config(
        app=app,
        host=settings.server_host,
        port=settings.server_port,
        workers=settings.server_workers,
        log_level=settings.log_level.lower(),
    )
    server = uvicorn.Server(config)
    
    try:
        await server.serve()
    except KeyboardInterrupt:
        logger.info("Shutting down monitoring system")
        scheduler_task.cancel()
        await server.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
