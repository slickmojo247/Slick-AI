# security/system.py
import asyncio
from typing import Dict, Optional
from dataclasses import dataclass
from enum import Enum

class SecurityLevel(Enum):
    NORMAL = 1
    SUSPICIOUS = 2
    MALICIOUS = 3

@dataclass
class SecurityEvent:
    source: str
    event_type: str
    severity: SecurityLevel
    metadata: Dict

class SecurityMonitor:
    def __init__(self):
        self.anomaly_detector = AnomalyDetection()
        self.alert_system = AlertSystem()
        self.knowledge_graph = KnowledgeGraph()
        
    async def monitor_event(self, event: SecurityEvent):
        """Process security events through full pipeline"""
        # Check for anomalies
        anomaly_score = await self.anomaly_detector.analyze(event)
        
        # Update knowledge graph
        await self.knowledge_graph.log_event(event, anomaly_score)
        
        # Trigger alerts if needed
        if anomaly_score > 0.7:
            await self.alert_system.trigger_alert(event, anomaly_score)

class MediationEngine:
    def __init__(self):
        self.security_monitor = SecurityMonitor()
        self.ai_services = AIServiceRouter()
        
    async def mediate_request(self, source: str, input_data: str) -> Optional[str]:
        """Process all requests through security mediation"""
        # Create security event
        event = SecurityEvent(
            source=source,
            event_type="API_REQUEST",
            severity=SecurityLevel.NORMAL,
            metadata={"input": input_data}
        )
        
        # Security screening
        await self.security_monitor.monitor_event(event)
        
        if event.severity == SecurityLevel.MALICIOUS:
            return None  # Block malicious requests
        
        # Route to appropriate AI service
        return await self.ai_services.route_request(input_data)

class AnomalyDetection:
    def __init__(self):
        self.behavior_profiles = BehaviorProfiles()
        
    async def analyze(self, event: SecurityEvent) -> float:
        """Calculate anomaly score (0-1)"""
        baseline = await self.behavior_profiles.get_baseline(event.source)
        deviation = self._calculate_deviation(event, baseline)
        return min(deviation * 1.5, 1.0)  # Cap at 1.0
        
    def _calculate_deviation(self, event: SecurityEvent, baseline: Dict) -> float:
        # Implementation from original security.py
        return 0.0  # Actual deviation calculation

class AlertSystem:
    async def trigger_alert(self, event: SecurityEvent, score: float):
        """Handle real-time alerting"""
        # Send to dashboard
        await SecurityDashboard.update(event, score)
        
        # Log to audit system
        AuditLogger.log_security_event(event, score)

class AIServiceRouter:
    async def route_request(self, input_data: str) -> str:
        """Route request to appropriate AI service"""
        # Implementation from original ai_routing.py
        return "Response from AI service"

class KnowledgeGraph:
    async def log_event(self, event: SecurityEvent, anomaly_score: float):
        """Update knowledge graph with security context"""
        # Implementation would connect to your existing knowledge graph
        pass

# Integration with existing components
class SecurityDashboard:
    @staticmethod
    async def update(event: SecurityEvent, score: float):
        """Update the web interface dashboard"""
        from interfaces.web import update_security_status
        await update_security_status(
            source=event.source,
            threat_level=score,
            last_event=event.event_type
        )

class AuditLogger:
    @staticmethod
    def log_security_event(event: SecurityEvent, score: float):
        """Log to persistent audit system"""
        from services.storage import SecurityLogDB
        SecurityLogDB.insert(
            timestamp=datetime.now(),
            event_type=event.event_type,
            severity=score,
            metadata=event.metadata
        )