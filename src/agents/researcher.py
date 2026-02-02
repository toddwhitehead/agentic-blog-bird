"""
Researcher Agent Module

This agent is responsible for collecting information from Microsoft Fabric
about bird detection events and data throughout the day.
"""

from typing import Dict, List, Any
import json
from datetime import datetime
from .base_agent import BaseAgent


class ResearcherAgent(BaseAgent):
    """
    Researcher agent that collects bird detection data from Microsoft Fabric.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the Researcher agent.
        
        Args:
            config: Configuration dictionary for Fabric connection and queries
        """
        super().__init__(name="Researcher", config=config)
        self._initialize_agent_client()
        
    def get_system_message(self) -> str:
        """Return the system message for the researcher agent."""
        return """You are a Researcher agent specialized in collecting and analyzing bird detection data.
        
Your responsibilities:
1. Query Microsoft Fabric for bird detection events from the day
2. Gather relevant telemetry data (detection times, species, counts, images)
3. Identify interesting patterns or notable events
4. Compile comprehensive data summaries for the writing team
5. Ensure all data is accurate and properly sourced

When collecting data, focus on:
- Species identified and their frequencies
- Notable or rare sightings
- Time-based patterns (peak activity times)
- Environmental conditions during detections
- Any unusual or interesting behaviors captured

Format your research summary with clear structure including:
- Total detections count
- Species breakdown
- Notable events or highlights
- Time distribution of activities
- Any relevant contextual information
"""
    
    def collect_bird_data(self, date: str = None) -> Dict[str, Any]:
        """
        Collect bird detection data from Microsoft Fabric.
        
        Args:
            date: Date to collect data for (YYYY-MM-DD format)
            
        Returns:
            Dictionary containing collected bird detection data
        """
        # In a real implementation, this would query Microsoft Fabric
        # For now, return a structured template
        
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
            
        return {
            "date": date,
            "total_detections": 0,
            "species_detected": [],
            "time_distribution": {},
            "notable_events": [],
            "environmental_conditions": {},
            "data_source": "Microsoft Fabric",
            "query_timestamp": datetime.now().isoformat()
        }
    
    def analyze_patterns(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze patterns in the collected data.
        
        Args:
            data: Raw bird detection data
            
        Returns:
            Dictionary containing pattern analysis
        """
        analysis = {
            "patterns": [],
            "insights": [],
            "highlights": []
        }
        
        # Add pattern analysis logic here
        return analysis
    
    def generate_research_summary(self, date: str = None) -> str:
        """
        Generate a comprehensive research summary.
        
        Args:
            date: Date to generate summary for
            
        Returns:
            Formatted research summary as a string
        """
        data = self.collect_bird_data(date)
        analysis = self.analyze_patterns(data)
        
        summary = f"""
# Research Summary for {data['date']}

## Overview
- Total Detections: {data['total_detections']}
- Unique Species: {len(data['species_detected'])}
- Data Source: {data['data_source']}
- Query Time: {data['query_timestamp']}

## Species Detected
{self._format_species_list(data['species_detected'])}

## Time Distribution
{self._format_time_distribution(data['time_distribution'])}

## Notable Events
{self._format_notable_events(data['notable_events'])}

## Patterns and Insights
{self._format_analysis(analysis)}

## Environmental Conditions
{self._format_environmental_data(data['environmental_conditions'])}
"""
        return summary
    
    def _format_species_list(self, species: List[str]) -> str:
        """Format species list for output."""
        if not species:
            return "No species detected"
        return "\n".join(f"- {s}" for s in species)
    
    def _format_time_distribution(self, distribution: Dict[str, int]) -> str:
        """Format time distribution data."""
        if not distribution:
            return "No time distribution data available"
        return "\n".join(f"- {time}: {count} detections" 
                        for time, count in distribution.items())
    
    def _format_notable_events(self, events: List[str]) -> str:
        """Format notable events."""
        if not events:
            return "No notable events recorded"
        return "\n".join(f"- {event}" for event in events)
    
    def _format_analysis(self, analysis: Dict[str, Any]) -> str:
        """Format analysis results."""
        output = []
        if analysis.get('patterns'):
            output.append("Patterns:")
            output.extend(f"- {p}" for p in analysis['patterns'])
        if analysis.get('insights'):
            output.append("\nInsights:")
            output.extend(f"- {i}" for i in analysis['insights'])
        return "\n".join(output) if output else "No patterns identified"
    
    def _format_environmental_data(self, conditions: Dict[str, Any]) -> str:
        """Format environmental conditions."""
        if not conditions:
            return "No environmental data available"
        return "\n".join(f"- {key}: {value}" 
                        for key, value in conditions.items())
