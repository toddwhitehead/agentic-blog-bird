"""
Researcher Agent Module

This agent is responsible for collecting information from Azure Blob Storage
about bird detection events and data files.
"""

from typing import Dict, List, Any
import json
import os
from datetime import datetime
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from .base_agent import BaseAgent


class ResearcherAgent(BaseAgent):
    """
    Researcher agent that collects bird detection data from Azure Blob Storage.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the Researcher agent.
        
        Args:
            config: Configuration dictionary for Blob Storage connection
        """
        super().__init__(name="Researcher", config=config)
        self._initialize_agent_client()
        self.blob_service_client = None
        self._initialize_blob_storage()
        
    def _initialize_blob_storage(self):
        """Initialize Azure Blob Storage client."""
        # Try to get connection string from environment variable first
        connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        
        # If not in environment, try config
        if not connection_string:
            connection_string = self.config.get("blob_storage_connection_string")
        
        if connection_string:
            try:
                self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
            except Exception as e:
                print(f"Warning: Could not initialize Blob Storage client: {e}")
                self.blob_service_client = None
        else:
            print("Warning: No Azure Storage connection string found. Blob storage access disabled.")
        
    def get_system_message(self) -> str:
        """Return the system message for the researcher agent."""
        return """You are a Researcher agent specialized in collecting and analyzing bird detection data.
        
Your responsibilities:
1. Retrieve bird detection data files from Azure Blob Storage
2. Parse and analyze data from JSON/CSV files (detection times, species, counts, images)
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
- Data file source information
"""
    
    def list_data_files(self) -> List[str]:
        """
        List all bird detection data files in blob storage.
        
        Returns:
            List of blob names (file paths)
        """
        if not self.blob_service_client:
            print("Warning: Blob storage not initialized. Returning empty list.")
            return []
        
        container_name = self.config.get("blob_container_name", "bird-detection-data")
        if not container_name:
            container_name = os.getenv("BLOB_CONTAINER_NAME", "bird-detection-data")
        
        try:
            container_client = self.blob_service_client.get_container_client(container_name)
            blob_list = container_client.list_blobs()
            
            # Filter for data files (JSON or CSV)
            data_files = []
            for blob in blob_list:
                if blob.name.endswith(('.json', '.csv')):
                    data_files.append(blob.name)
            
            return data_files
        except Exception as e:
            print(f"Error listing blobs: {e}")
            return []
    
    def download_data_file(self, blob_name: str) -> Dict[str, Any]:
        """
        Download and parse a bird detection data file from blob storage.
        
        Args:
            blob_name: Name of the blob to download
            
        Returns:
            Dictionary containing parsed bird detection data
        """
        if not self.blob_service_client:
            print(f"Warning: Blob storage not initialized. Cannot download {blob_name}")
            return {}
        
        container_name = self.config.get("blob_container_name", "bird-detection-data")
        if not container_name:
            container_name = os.getenv("BLOB_CONTAINER_NAME", "bird-detection-data")
        
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=container_name, 
                blob=blob_name
            )
            
            # Download blob content
            blob_data = blob_client.download_blob().readall()
            
            # Parse based on file type
            if blob_name.endswith('.json'):
                data = json.loads(blob_data.decode('utf-8'))
            elif blob_name.endswith('.csv'):
                # For CSV files, we'll read them as text and convert to simple format
                # In a real implementation, you might use pandas or csv module
                data = self._parse_csv_data(blob_data.decode('utf-8'))
            else:
                data = {}
            
            # Add metadata
            if isinstance(data, dict):
                data['source_file'] = blob_name
                data['download_timestamp'] = datetime.now().isoformat()
            
            return data
            
        except Exception as e:
            print(f"Error downloading blob {blob_name}: {e}")
            return {}
    
    def _parse_csv_data(self, csv_content: str) -> Dict[str, Any]:
        """
        Parse CSV data into structured format.
        
        Args:
            csv_content: CSV content as string
            
        Returns:
            Dictionary containing parsed data
        """
        lines = csv_content.strip().split('\n')
        if len(lines) < 2:
            return {}
        
        # Simple CSV parser - assumes first row is headers
        headers = [h.strip() for h in lines[0].split(',')]
        rows = []
        
        for line in lines[1:]:
            values = [v.strip() for v in line.split(',')]
            if len(values) == len(headers):
                row = dict(zip(headers, values))
                rows.append(row)
        
        return {
            'data': rows,
            'format': 'csv',
            'row_count': len(rows)
        }
    
    def collect_bird_data_from_file(self, blob_name: str) -> Dict[str, Any]:
        """
        Collect and structure bird detection data from a specific file.
        
        Args:
            blob_name: Name of the blob file to process
            
        Returns:
            Dictionary containing structured bird detection data
        """
        raw_data = self.download_data_file(blob_name)
        
        if not raw_data:
            return {
                "source_file": blob_name,
                "total_detections": 0,
                "species_detected": [],
                "time_distribution": {},
                "notable_events": [],
                "environmental_conditions": {},
                "data_source": "Azure Blob Storage",
                "query_timestamp": datetime.now().isoformat(),
                "error": "Failed to download or parse file"
            }
        
        # Extract structured information from raw data
        # The structure depends on the actual format of the files
        # This is a flexible parser that handles various formats
        
        result = {
            "source_file": blob_name,
            "total_detections": 0,
            "species_detected": [],
            "time_distribution": {},
            "notable_events": [],
            "environmental_conditions": {},
            "data_source": "Azure Blob Storage",
            "query_timestamp": datetime.now().isoformat()
        }
        
        # Try to extract common fields
        if 'detections' in raw_data:
            detections = raw_data['detections']
            if isinstance(detections, list):
                result['total_detections'] = len(detections)
                # Extract species
                species_set = set()
                for detection in detections:
                    if 'species' in detection:
                        species_set.add(detection['species'])
                result['species_detected'] = list(species_set)
        
        if 'species' in raw_data:
            result['species_detected'] = raw_data['species'] if isinstance(raw_data['species'], list) else [raw_data['species']]
        
        if 'total_detections' in raw_data:
            result['total_detections'] = raw_data['total_detections']
        
        if 'date' in raw_data:
            result['date'] = raw_data['date']
        
        if 'notable_events' in raw_data:
            result['notable_events'] = raw_data['notable_events']
        
        if 'environmental_conditions' in raw_data:
            result['environmental_conditions'] = raw_data['environmental_conditions']
        
        # For CSV format
        if raw_data.get('format') == 'csv' and 'data' in raw_data:
            result['total_detections'] = raw_data['row_count']
            # Extract species from CSV rows
            species_set = set()
            for row in raw_data['data']:
                if 'species' in row:
                    species_set.add(row['species'])
            if species_set:
                result['species_detected'] = list(species_set)
        
        return result
    
    def collect_bird_data(self, date: str = None) -> Dict[str, Any]:
        """
        Collect bird detection data from Azure Blob Storage.
        For backward compatibility - returns data from first available file.
        
        Args:
            date: Date to collect data for (YYYY-MM-DD format) - optional
            
        Returns:
            Dictionary containing collected bird detection data
        """
        # List all data files
        data_files = self.list_data_files()
        
        if not data_files:
            # Return empty structure if no files found
            if date is None:
                date = datetime.now().strftime("%Y-%m-%d")
            return {
                "date": date,
                "total_detections": 0,
                "species_detected": [],
                "time_distribution": {},
                "notable_events": [],
                "environmental_conditions": {},
                "data_source": "Azure Blob Storage",
                "query_timestamp": datetime.now().isoformat(),
                "note": "No data files found in blob storage"
            }
        
        # Use the first file for backward compatibility
        return self.collect_bird_data_from_file(data_files[0])
    
    def collect_all_bird_data(self) -> List[Dict[str, Any]]:
        """
        Collect bird detection data from all files in blob storage.
        
        Returns:
            List of dictionaries, each containing data from one file
        """
        data_files = self.list_data_files()
        all_data = []
        
        print(f"Researcher: Found {len(data_files)} data files in blob storage")
        
        for blob_name in data_files:
            print(f"Researcher: Processing {blob_name}...")
            data = self.collect_bird_data_from_file(blob_name)
            all_data.append(data)
        
        return all_data
    
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
        For backward compatibility - generates summary for first file.
        
        Args:
            date: Date to generate summary for
            
        Returns:
            Formatted research summary as a string
        """
        data = self.collect_bird_data(date)
        analysis = self.analyze_patterns(data)
        
        summary = f"""
# Research Summary for {data.get('date', 'Unknown Date')}

## Overview
- Total Detections: {data['total_detections']}
- Unique Species: {len(data['species_detected'])}
- Data Source: {data['data_source']}
- Source File: {data.get('source_file', 'N/A')}
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
    
    def generate_research_summary_for_file(self, blob_name: str) -> str:
        """
        Generate a comprehensive research summary for a specific data file.
        
        Args:
            blob_name: Name of the blob file to generate summary for
            
        Returns:
            Formatted research summary as a string
        """
        data = self.collect_bird_data_from_file(blob_name)
        analysis = self.analyze_patterns(data)
        
        summary = f"""
# Research Summary for {blob_name}

## Overview
- Source File: {data.get('source_file', blob_name)}
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
    
    def generate_all_research_summaries(self) -> List[Dict[str, str]]:
        """
        Generate research summaries for all data files in blob storage.
        
        Returns:
            List of dictionaries with 'file' and 'summary' keys
        """
        data_files = self.list_data_files()
        summaries = []
        
        for blob_name in data_files:
            summary = self.generate_research_summary_for_file(blob_name)
            summaries.append({
                'file': blob_name,
                'summary': summary
            })
        
        return summaries
    
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
