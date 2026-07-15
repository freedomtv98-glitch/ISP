"""Configuration management for ISP monitoring system."""

from typing import List, Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Server Configuration
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    server_workers: int = 4
    server_debug: bool = False

    # Environment
    environment: str = "development"
    log_level: str = "INFO"

    # Database Configuration
    influxdb_url: str = "http://localhost:8086"
    influxdb_org: str = "isp-monitoring"
    influxdb_bucket: str = "network-metrics"
    influxdb_token: str = ""

    # Redis Configuration
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: Optional[str] = None

    # Monitoring Configuration
    monitor_interval: int = 60
    monitor_timeout: int = 30
    metric_retention_days: int = 30

    # Alert Configuration
    alert_enabled: bool = True
    alert_email_enabled: bool = True
    alert_slack_enabled: bool = False
    alert_email_from: str = "alerts@isp-monitor.local"
    alert_email_smtp_server: str = "localhost"
    alert_email_smtp_port: int = 587

    # Slack Integration
    slack_webhook_url: str = ""
    slack_channel: str = "#network-alerts"

    # API Configuration
    api_title: str = "ISP Network Monitoring API"
    api_version: str = "1.0.0"
    api_description: str = "Real-time network monitoring and alerting system"

    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
