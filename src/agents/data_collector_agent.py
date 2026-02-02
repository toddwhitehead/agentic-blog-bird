"""
Data Collector Agent for processing telemetry and notifications
Uses Microsoft Agent Framework with Azure AI Foundry
"""
from typing import Any, Dict, List
import logging
from datetime import datetime
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class DataCollectorAgent(BaseAgent):
    """
    Agent specialized in collecting and processing telemetry data
    and IoT notifications from the backyard monitoring system
    """
    
    def __init__(self, name: str = "DataCollector", model_deployment: str = "gpt-4"):
        """Initialize the Data Collector Agent"""
        description = (
            "An AI agent specialized in collecting, processing, and analyzing "
            "telemetry data and notifications from IoT devices. You excel at "
            "identifying patterns, anomalies, and interesting events in sensor data."
        )
        super().__init__(name, description, model_deployment)
        self.collected_data: List[Dict[str, Any]] = []
    
    def get_system_prompt(self) -> str:
        """Get the specialized system prompt for data collection"""
        return (
            f"{super().get_system_prompt()}\n\n"
            "Your role is to:\n"
            "1. Collect telemetry data from various IoT sensors\n"
            "2. Process and normalize incoming notifications\n"
            "3. Identify interesting patterns and anomalies\n"
            "4. Summarize key events and trends\n"
            "5. Prepare data for blog content generation\n\n"
            "Focus on extracting meaningful insights from raw sensor data."
        )
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process incoming telemetry data and notifications
        
        Args:
            input_data: Contains message and raw telemetry data
            
        Returns:
            Dict with processed data and summary
        """
        message = input_data.get("message", "")
        context = input_data.get("context", {})
        raw_data = context.get("raw_telemetry", {})
        
        logger.info(f"[{self.name}] Processing telemetry data")
        
        # Process the raw data
        processed_data = self._process_telemetry(raw_data)
        
        # Generate summary
        summary = self._generate_summary(processed_data)
        
        # Store for future reference
        self.collected_data.append({
            "timestamp": datetime.now().isoformat(),
            "processed": processed_data,
            "summary": summary
        })
        
        logger.info(f"[{self.name}] Processed {len(processed_data.get('events', []))} events")
        
        return {
            "response": summary,
            "processed_data": processed_data,
            "metadata": {
                "agent": self.name,
                "event_count": len(processed_data.get("events", [])),
                "timestamp": datetime.now().isoformat()
            }
        }
    
    def _process_telemetry(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process raw telemetry data
        
        Note: In production, this could use Azure AI for anomaly detection
        and pattern recognition
        """
        events = []
        
        # Extract events from raw data
        if "sensors" in raw_data:
            for sensor_name, sensor_data in raw_data.get("sensors", {}).items():
                value = sensor_data.get("value")
                timestamp = sensor_data.get("timestamp", datetime.now().isoformat())
                
                events.append({
                    "type": "sensor_reading",
                    "sensor": sensor_name,
                    "value": value,
                    "timestamp": timestamp,
                    "description": f"{sensor_name} recorded: {value}"
                })
        
        # Extract notifications
        if "notifications" in raw_data:
            for notification in raw_data.get("notifications", []):
                events.append({
                    "type": "notification",
                    "message": notification.get("message", ""),
                    "priority": notification.get("priority", "normal"),
                    "timestamp": notification.get("timestamp", datetime.now().isoformat()),
                    "description": notification.get("message", "System notification")
                })
        
        return {
            "events": events,
            "total_count": len(events),
            "timeframe": {
                "start": min([e["timestamp"] for e in events]) if events else None,
                "end": max([e["timestamp"] for e in events]) if events else None
            }
        }
    
    def _generate_summary(self, processed_data: Dict[str, Any]) -> str:
        """Generate a summary of the processed data"""
        events = processed_data.get("events", [])
        
        if not events:
            return "No significant events detected during this period."
        
        # Count event types
        sensor_readings = sum(1 for e in events if e.get("type") == "sensor_reading")
        notifications = sum(1 for e in events if e.get("type") == "notification")
        
        # Build summary sentence
        summary = f"Collected {len(events)} events from the backyard monitoring system"
        
        if sensor_readings > 0 and notifications > 0:
            summary += f". {sensor_readings} sensor readings were recorded and {notifications} notifications were received."
        elif sensor_readings > 0:
            summary += f". {sensor_readings} sensor readings were recorded."
        elif notifications > 0:
            summary += f". {notifications} notifications were received."
        else:
            summary += "."
        
        return summary
    
    def get_collected_data(self) -> List[Dict[str, Any]]:
        """Get all collected data"""
        return self.collected_data
    
    def clear_collected_data(self):
        """Clear collected data"""
        self.collected_data = []
        logger.info(f"[{self.name}] Cleared collected data")
