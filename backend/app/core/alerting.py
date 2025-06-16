import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ...core.config import settings

logger = logging.getLogger(__name__)

class AlertManager:
    def __init__(self):
        self.alert_history: List[Dict[str, Any]] = []
        self.alert_thresholds = {
            "cpu_usage": 80,
            "memory_usage": 80,
            "disk_usage": 80,
            "error_rate": 5,  # percentage
            "response_time": 2.0  # seconds
        }

    def check_metrics(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Check metrics against thresholds and generate alerts
        """
        alerts = []
        
        # Check system metrics
        if metrics.get("cpu_usage", 0) > self.alert_thresholds["cpu_usage"]:
            alerts.append({
                "level": "warning",
                "component": "system",
                "metric": "cpu_usage",
                "value": metrics["cpu_usage"],
                "threshold": self.alert_thresholds["cpu_usage"],
                "message": f"High CPU usage detected: {metrics['cpu_usage']}%"
            })

        if metrics.get("memory_usage", 0) > self.alert_thresholds["memory_usage"]:
            alerts.append({
                "level": "warning",
                "component": "system",
                "metric": "memory_usage",
                "value": metrics["memory_usage"],
                "threshold": self.alert_thresholds["memory_usage"],
                "message": f"High memory usage detected: {metrics['memory_usage']}%"
            })

        if metrics.get("disk_usage", 0) > self.alert_thresholds["disk_usage"]:
            alerts.append({
                "level": "warning",
                "component": "system",
                "metric": "disk_usage",
                "value": metrics["disk_usage"],
                "threshold": self.alert_thresholds["disk_usage"],
                "message": f"High disk usage detected: {metrics['disk_usage']}%"
            })

        # Check application metrics
        if metrics.get("error_rate", 0) > self.alert_thresholds["error_rate"]:
            alerts.append({
                "level": "error",
                "component": "application",
                "metric": "error_rate",
                "value": metrics["error_rate"],
                "threshold": self.alert_thresholds["error_rate"],
                "message": f"High error rate detected: {metrics['error_rate']}%"
            })

        if metrics.get("response_time", 0) > self.alert_thresholds["response_time"]:
            alerts.append({
                "level": "warning",
                "component": "application",
                "metric": "response_time",
                "value": metrics["response_time"],
                "threshold": self.alert_thresholds["response_time"],
                "message": f"High response time detected: {metrics['response_time']}s"
            })

        return alerts

    def process_alerts(self, alerts: List[Dict[str, Any]]) -> None:
        """
        Process alerts and send notifications
        """
        for alert in alerts:
            # Log the alert
            logger.warning(f"Alert: {alert['message']}")
            
            # Store in history
            self.alert_history.append({
                **alert,
                "timestamp": datetime.utcnow().isoformat()
            })

            # Send email notification for critical alerts
            if alert["level"] == "error":
                self.send_email_alert(alert)

    def send_email_alert(self, alert: Dict[str, Any]) -> None:
        """
        Send email notification for critical alerts
        """
        if not settings.SMTP_HOST or not settings.SMTP_PORT:
            logger.warning("SMTP settings not configured, skipping email alert")
            return

        try:
            msg = MIMEMultipart()
            msg["From"] = settings.SMTP_USER
            msg["To"] = settings.ALERT_EMAIL_RECIPIENTS
            msg["Subject"] = f"Critical Alert: {alert['component']} - {alert['metric']}"

            body = f"""
            Critical Alert Detected:
            
            Component: {alert['component']}
            Metric: {alert['metric']}
            Value: {alert['value']}
            Threshold: {alert['threshold']}
            Message: {alert['message']}
            Time: {datetime.utcnow().isoformat()}
            """

            msg.attach(MIMEText(body, "plain"))

            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                if settings.SMTP_USER and settings.SMTP_PASSWORD:
                    server.starttls()
                    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)

            logger.info(f"Email alert sent for {alert['metric']}")
        except Exception as e:
            logger.error(f"Failed to send email alert: {str(e)}")

    def get_alert_history(
        self,
        component: Optional[str] = None,
        level: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get alert history with optional filtering
        """
        filtered_history = self.alert_history

        if component:
            filtered_history = [
                alert for alert in filtered_history
                if alert["component"] == component
            ]

        if level:
            filtered_history = [
                alert for alert in filtered_history
                if alert["level"] == level
            ]

        return filtered_history[-limit:]

# Create a global alert manager instance
alert_manager = AlertManager() 