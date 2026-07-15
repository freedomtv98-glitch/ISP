"""Time-series database interface."""

import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class TimeSeriesDB(ABC):
    """Abstract base class for time-series databases."""

    @abstractmethod
    async def write(
        self,
        measurement: str,
        tags: Dict[str, str],
        fields: Dict[str, Any],
        timestamp: Optional[datetime] = None,
    ) -> bool:
        """Write metric to database."""
        pass

    @abstractmethod
    async def query(
        self,
        measurement: str,
        start_time: datetime,
        end_time: datetime,
        filters: Optional[Dict[str, str]] = None,
    ) -> List[Dict[str, Any]]:
        """Query metrics from database."""
        pass


class InfluxDBConnector(TimeSeriesDB):
    """InfluxDB time-series connector."""

    def __init__(self, url: str, org: str, bucket: str, token: str):
        """Initialize InfluxDB connector.
        
        Args:
            url: InfluxDB server URL
            org: Organization name
            bucket: Bucket name
            token: Authentication token
        """
        self.url = url
        self.org = org
        self.bucket = bucket
        self.token = token
        self.client = None

    async def connect(self) -> None:
        """Connect to InfluxDB."""
        try:
            from influxdb_client import InfluxDBClient
            self.client = InfluxDBClient(
                url=self.url,
                org=self.org,
                token=self.token,
            )
            logger.info(f"Connected to InfluxDB at {self.url}")
        except Exception as e:
            logger.error(f"Failed to connect to InfluxDB: {e}")
            raise

    async def disconnect(self) -> None:
        """Disconnect from InfluxDB."""
        if self.client:
            self.client.close()
            logger.info("Disconnected from InfluxDB")

    async def write(
        self,
        measurement: str,
        tags: Dict[str, str],
        fields: Dict[str, Any],
        timestamp: Optional[datetime] = None,
    ) -> bool:
        """Write metric to InfluxDB."""
        try:
            from influxdb_client.client.write_api import SYNCHRONOUS
            
            write_api = self.client.write_api(write_options=SYNCHRONOUS)
            
            point_dict = {
                "measurement": measurement,
                "tags": tags,
                "fields": fields,
            }
            if timestamp:
                point_dict["time"] = timestamp
            
            write_api.write(self.bucket, self.org, point_dict)
            return True
        except Exception as e:
            logger.error(f"Error writing to InfluxDB: {e}")
            return False

    async def query(
        self,
        measurement: str,
        start_time: datetime,
        end_time: datetime,
        filters: Optional[Dict[str, str]] = None,
    ) -> List[Dict[str, Any]]:
        """Query metrics from InfluxDB."""
        try:
            query_api = self.client.query_api()
            # Simplified query - implement full query logic as needed
            query = f'from(bucket:"{self.bucket}") |> range(start: {start_time}, stop: {end_time})'
            result = query_api.query(query, org=self.org)
            return result
        except Exception as e:
            logger.error(f"Error querying InfluxDB: {e}")
            return []
