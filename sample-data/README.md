# Sample Bird Event Data

This directory contains sample bird detection event data for testing and demonstration purposes.

## File Formats

### JSON Format
The JSON files contain comprehensive bird detection data with the following structure:
- `date`: Date of observations (YYYY-MM-DD)
- `total_detections`: Total number of bird detections
- `species`: List of unique species detected
- `detections`: Array of individual detection events with:
  - `species`: Bird species name
  - `time`: Time of detection (HH:MM:SS)
  - `confidence`: AI confidence score (0.0-1.0)
  - `behavior`: Observed behavior
  - `location`: Detection location in backyard
- `notable_events`: List of interesting observations
- `environmental_conditions`: Weather and environmental data
- `equipment_status`: System performance metrics

### CSV Format
The CSV files contain simplified detection records with columns:
- `species`: Bird species name
- `time`: Time of detection (HH:MM:SS)
- `confidence`: AI confidence score (0.0-1.0)
- `behavior`: Observed behavior
- `location`: Detection location in backyard

## Sample Files

- `bird-events-2024-01-15.json` - Full day of observations with Cardinals, Blue Jays, Robins, and more
- `bird-events-2024-01-16.json` - Observations including rare Downy Woodpecker and courtship behaviors
- `bird-events-2024-01-17.csv` - CSV format data with Goldfinches, Nuthatches, and Winter species

## Using Sample Data

The Researcher agent automatically looks for sample data in this folder when Azure Blob Storage is not configured. This allows for:
- Testing the multi-agent system locally
- Demonstration without cloud dependencies
- Development and debugging workflows
- Example data structure reference

## Species Featured

These sample files include common North American backyard bird species:
- Northern Cardinal
- Blue Jay
- American Robin
- House Sparrow
- Black-capped Chickadee
- Mourning Dove
- Tufted Titmouse
- Downy Woodpecker
- House Finch
- American Goldfinch
- Dark-eyed Junco
- Carolina Wren
- White-breasted Nuthatch

All detection data is representative of typical backyard bird monitoring scenarios with realistic behaviors, times, and environmental conditions.
