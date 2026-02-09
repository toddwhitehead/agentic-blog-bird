# Azure Blob Storage Integration Guide

This guide explains how to use the Azure Blob Storage integration for bird detection data in the Agentic Blog Bird system.

## Overview

The system now retrieves bird detection data from Azure Blob Storage instead of Microsoft Fabric. Each data file in the blob storage can be processed to generate a separate blog post.

## Prerequisites

- Azure Storage Account
- Blob container created (default name: `bird-detection-data`)
- Bird detection data files uploaded to the container

## Configuration

### 1. Environment Variables

Add the following to your `.env` file:

```bash
# Azure Blob Storage Configuration
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=your_account;AccountKey=your_key;EndpointSuffix=core.windows.net
AZURE_STORAGE_ACCOUNT_NAME=your_storage_account_name
BLOB_CONTAINER_NAME=bird-detection-data
```

### 2. Configuration File

Update `config/config.yaml`:

```yaml
researcher:
  blob_storage_account: "your_account_name"
  blob_container_name: "bird-detection-data"
  blob_storage_connection_string: ""  # Optional, will use env var if not set
```

## Data File Formats

The system supports two data file formats:

### JSON Format

```json
{
  "date": "2024-01-15",
  "total_detections": 42,
  "species": ["Cardinal", "Blue Jay", "Sparrow"],
  "detections": [
    {
      "species": "Cardinal",
      "time": "08:30:00",
      "confidence": 0.95
    },
    {
      "species": "Blue Jay",
      "time": "09:15:00",
      "confidence": 0.92
    }
  ],
  "notable_events": [
    "First Cardinal sighting of the day",
    "Blue Jay observed at feeder"
  ],
  "environmental_conditions": {
    "temperature": "45F",
    "weather": "sunny",
    "wind": "light breeze"
  }
}
```

### CSV Format

```csv
species,time,confidence,location
Cardinal,08:30:00,0.95,"Backyard, Near Feeder"
Blue Jay,09:15:00,0.92,"Tree, Upper branch"
Sparrow,10:00:00,0.88,Ground
```

## Usage

### Single Blog Post Mode (Backward Compatible)

Process the first data file found:

```bash
python main.py
```

or for a specific date:

```bash
python main.py --date 2024-01-15
```

### Multiple Blog Post Mode

Process all data files in blob storage (one blog post per file):

```bash
python main.py --all-files
```

With custom output directory:

```bash
python main.py --all-files --output-dir content/posts
```

With verbose output:

```bash
python main.py --all-files --verbose
```

## Programmatic Usage

### Example 1: List Data Files

```python
from agents import ResearcherAgent

researcher = ResearcherAgent({
    'blob_container_name': 'bird-detection-data'
})

# List all data files
files = researcher.list_data_files()
print(f"Found {len(files)} data files:")
for file in files:
    print(f"  - {file}")
```

### Example 2: Process Single File

```python
from agents import ResearcherAgent

researcher = ResearcherAgent()

# Collect data from a specific file
data = researcher.collect_bird_data_from_file('2024-01-15.json')
print(f"Total detections: {data['total_detections']}")
print(f"Species: {data['species_detected']}")

# Generate research summary
summary = researcher.generate_research_summary_for_file('2024-01-15.json')
print(summary)
```

### Example 3: Process All Files

```python
from agents import ResearcherAgent

researcher = ResearcherAgent()

# Collect data from all files
all_data = researcher.collect_all_bird_data()
print(f"Processed {len(all_data)} files")

for data in all_data:
    print(f"\nFile: {data['source_file']}")
    print(f"Detections: {data['total_detections']}")
    print(f"Species: {', '.join(data['species_detected'])}")
```

### Example 4: Generate Multiple Blog Posts

```python
from agents import EditorAgent

editor = EditorAgent({
    'publisher': {
        'output_dir': 'content/posts'
    }
})

# Create blog posts for all data files
result = editor.orchestrate_multiple_blog_creation()

print(f"Total files: {result['total_files']}")
print(f"Posts created: {result['posts_created']}")
print(f"Posts failed: {result['posts_failed']}")

# Display results
for post in result['posts']:
    if post['status'] == 'completed':
        print(f"✓ {post['file']} -> {post['output_path']}")
    else:
        print(f"✗ {post['file']} - {post.get('reason', 'Unknown error')}")
```

## Uploading Data to Blob Storage

### Using Azure Portal

1. Navigate to your Storage Account
2. Open Blob Containers
3. Select your container (e.g., `bird-detection-data`)
4. Click "Upload"
5. Select your JSON or CSV files
6. Click "Upload"

### Using Azure CLI

```bash
# Upload a single file
az storage blob upload \
  --account-name your_account_name \
  --container-name bird-detection-data \
  --name 2024-01-15.json \
  --file /path/to/2024-01-15.json

# Upload multiple files
az storage blob upload-batch \
  --account-name your_account_name \
  --destination bird-detection-data \
  --source /path/to/data/files/
```

### Using Python

```python
from azure.storage.blob import BlobServiceClient

connection_string = "your_connection_string"
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client("bird-detection-data")

# Upload a file
with open("2024-01-15.json", "rb") as data:
    container_client.upload_blob(
        name="2024-01-15.json",
        data=data,
        overwrite=True
    )
```

## Troubleshooting

### Error: "No Azure Storage connection string found"

**Solution:** Ensure `AZURE_STORAGE_CONNECTION_STRING` is set in your `.env` file or environment variables.

### Error: "No data files found in blob storage"

**Solution:** 
1. Verify files are uploaded to the correct container
2. Check that files have `.json` or `.csv` extensions
3. Verify the container name matches your configuration

### Error: "Failed to download or parse file"

**Solution:**
1. Verify file format is valid JSON or CSV
2. Check file permissions in blob storage
3. Ensure connection string has read permissions

### Warning: "Blob storage not initialized"

**Solution:** This is expected if running without credentials (e.g., in testing). The system will return empty data structures gracefully.

## Best Practices

1. **File Naming**: Use descriptive names with dates (e.g., `2024-01-15-backyard.json`)
2. **Data Structure**: Use the JSON format for complex data with nested structures
3. **CSV Format**: Use CSV for simple tabular data
4. **File Size**: Keep individual files under 10MB for optimal processing
5. **Batch Processing**: Use `--all-files` flag to process multiple files efficiently
6. **Error Handling**: Always check the `status` field in results to handle failures

## Security Considerations

1. **Connection Strings**: Never commit connection strings to version control
2. **Access Keys**: Use Azure Key Vault for production deployments
3. **Managed Identity**: Consider using Managed Identity for Azure resources
4. **Permissions**: Grant minimum required permissions (read-only for data files)
5. **Network Security**: Use private endpoints for production blob storage

## Migration from Microsoft Fabric

If you were previously using Microsoft Fabric:

1. Export your data from Fabric to JSON or CSV format
2. Upload the exported files to blob storage
3. Update your configuration to use blob storage settings
4. The system maintains backward compatibility with existing workflows

## Support

For issues or questions:
- Check the main README.md for general setup
- Review this guide for blob storage-specific issues
- Open an issue on GitHub for bugs or feature requests
