#!/usr/bin/env python
"""Initialize database and create initial buckets."""

import os
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import logging
from influxdb_client import InfluxDBClient
from influxdb_client.client.bucket import BucketRetentionRules
from influxdb_client.client.write_api import SYNCHRONOUS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_influxdb():
    """Initialize InfluxDB with buckets and retention policies."""
    url = os.getenv('INFLUXDB_URL', 'http://localhost:8086')
    token = os.getenv('INFLUXDB_TOKEN', 'isp-monitoring-token')
    org = os.getenv('INFLUXDB_ORG', 'isp-monitoring')
    bucket = os.getenv('INFLUXDB_BUCKET', 'network-metrics')
    
    try:
        client = InfluxDBClient(url=url, token=token, org=org)
        
        # Verify connection
        ready = client.ready()
        if ready.status == 'ready':
            logger.info(f"Connected to InfluxDB at {url}")
        
        # Create organization if needed
        orgs_api = client.organizations_api()
        try:
            org_obj = orgs_api.find_organization_by_name(org)
            logger.info(f"Using existing organization: {org}")
        except:
            org_obj = orgs_api.create_organization(name=org)
            logger.info(f"Created organization: {org}")
        
        # Create bucket with retention policy
        buckets_api = client.buckets_api()
        try:
            bucket_obj = buckets_api.find_bucket_by_name(bucket)
            logger.info(f"Using existing bucket: {bucket}")
        except:
            retention_rules = BucketRetentionRules(type="expire", every_seconds=2592000)  # 30 days
            bucket_obj = buckets_api.create_bucket(
                bucket_name=bucket,
                retention_rules=retention_rules,
                org_id=org_obj.id
            )
            logger.info(f"Created bucket: {bucket} with 30-day retention")
        
        client.close()
        logger.info("Database initialization completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize InfluxDB: {e}")
        return False


if __name__ == "__main__":
    success = init_influxdb()
    sys.exit(0 if success else 1)
