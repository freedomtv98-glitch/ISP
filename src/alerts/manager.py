"""Alert manager for handling threshold violations."""

import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class Alert:
    """Alert model."""

    def __init__(
        self,
        alert_id: str,
        name: str,
        severity: str,
        message: str,
    ):
        """Initialize alert."""
        self.id = alert_id
        self.name = name
        self.severity = severity
        self.message = message
        self.timestamp = datetime.utcnow()
        self.resolved = False


class AlertManager:
    """Manages alert lifecycle and notifications."""

    def __init__(self):
        """Initialize alert manager."""
        self.active_alerts: Dict[str, Alert] = {}
        self.alert_history: List[Alert] = []

    async def create_alert(
        self,
        alert_id: str,
        name: str,
        severity: str,
        message: str,
    ) -> Alert:
        """Create and store an alert."""
        alert = Alert(alert_id, name, severity, message)
        self.active_alerts[alert_id] = alert
        logger.warning(f"Alert created: {name} - {message}")
        return alert

    async def resolve_alert(self, alert_id: str) -> Optional[Alert]:
        """Resolve an active alert."""
        if alert_id in self.active_alerts:
            alert = self.active_alerts.pop(alert_id)
            alert.resolved = True
            self.alert_history.append(alert)
            logger.info(f"Alert resolved: {alert.name}")
            return alert
        return None

    def get_active_alerts(self) -> List[Alert]:
        """Get all active alerts."""
        return list(self.active_alerts.values())
