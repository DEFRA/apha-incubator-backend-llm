# Text Summarisation API - CDP Backend

A FastAPI-based backend service for summarising text using AWS Bedrock. Built for CDP (Customer Data Platform) integration.

## Features

- **Text Summarisation**: Summarise any plain text using AWS Bedrock (Claude 3)
- **REST API**: FastAPI-based HTTP endpoints for easy integration
- **Token Tracking**: Returns input/output token counts for cost monitoring
- **Configuration Management**: Environment-based configuration with .env support
- **Short-term API Key Auth**: Uses AWS bearer token for authentication
- **CORS Support**: Enabled for cross-origin requests
- **Health Checks**: Built-in endpoint for service health monitoring
- **Comprehensive Testing**: Unit tests with pytest

## Project Structure

```
summarise-data-llm/
├── src/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration management
│   ├── models.py               # Pydantic data models
│   └── bedrock_summarizer.py   # AWS Bedrock integration
├── tests/
│   ├── __init__.py
│   └── test_api.py             # Test suite
├── requirements.txt            # Python dependencies
├── .env                        # Environment configuration (local)
├── .env.example                # Example environment file
└── README.md                   # This file
```

## Prerequisites

- Python 3.8+
- AWS Account with Bedrock access
- Short-term API key (AWS_BEARER_TOKEN_BEDROCK)

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and update with your AWS credentials:

```bash
cp .env.example .env
```

Edit `.env` and replace:
- `AWS_BEARER_TOKEN_BEDROCK`: Your AWS short-term API key
- `AWS_REGION`: Your AWS region (default: us-east-1)
- `BEDROCK_MODEL_ID`: Claude model ID (default: anthropic.claude-3-sonnet-20240229-v1:0)

### 3. Run the API

```bash
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

## API Endpoints

### Health Check
- **Endpoint**: `GET /health`
- **Description**: Check if the API is running and healthy

**Example Request:**
```bash
curl http://localhost:8000/health
```

**Example Response:**
```json
{
  "status": "healthy",
  "service": "text-summarisation-api",
  "model": "anthropic.claude-3-sonnet-20240229-v1:0"
}
```

### Get Configuration
- **Endpoint**: `GET /config`
- **Description**: Get current API configuration (non-sensitive values)

**Example Request:**
```bash
curl http://localhost:8000/config
```

**Example Response:**
```json
{
  "region": "us-east-1",
  "model_id": "anthropic.claude-3-sonnet-20240229-v1:0",
  "api_host": "0.0.0.0",
  "api_port": 8000
}
```

### Summarise Text
- **Endpoint**: `POST /summarise`
- **Description**: Summarise provided text using AWS Bedrock

**Request Body:**
```json
{
  "text": "Your text to summarise here. This can be a long document, article, or any plain text.",
  "max_length": 100
}
```

**Parameters:**
- `text` (required): The text to summarise (minimum 1 character)
- `max_length` (optional): Maximum length of summary in words (default: 100, range: 50-1000)

**Example Request:**
```bash
curl -X POST http://localhost:8000/summarise \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Artificial intelligence has transformed various industries. Machine learning models can now process vast amounts of data to identify patterns and make predictions. Natural language processing enables computers to understand and generate human language. These technologies are revolutionizing healthcare, finance, and education.",
    "max_length": 50
  }'
```

**Example Response:**
```json
{
  "original_text": "Artificial intelligence has transformed various industries...",
  "summary": "AI and machine learning are revolutionizing industries by processing data to identify patterns and make predictions. NLP enables computers to understand human language, transforming healthcare, finance, and education.",
  "model": "anthropic.claude-3-sonnet-20240229-v1:0",
  "input_tokens": 127,
  "output_tokens": 45
}
```

**Error Response (400):**
```json
{
  "error": "Invalid input",
  "detail": "text field is required",
  "code": "HTTP_400"
}
```

## Authentication

The API uses AWS Bearer Token authentication. The token is configured via the `AWS_BEARER_TOKEN_BEDROCK` environment variable in your `.env` file.

**Security Notes:**
- Never commit your `.env` file to version control
- Keep your AWS API keys secure
- Use short-term credentials when possible
- For production, use AWS IAM roles instead of bearer tokens

## Testing

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Test

```bash
pytest tests/test_api.py::test_health_check -v
```

### Run Tests with Coverage

```bash
pip install pytest-cov
pytest tests/ --cov=src --cov-report=html
```

## Development

### Install Development Dependencies

```bash
pip install -r requirements.txt
pip install pytest pytest-cov
```

### Auto-reload During Development

```bash
python -m uvicorn src.main:app --reload
```

### Debug Mode

Set environment variables:
```bash
export DEBUG=True
python -m uvicorn src.main:app --reload
```

## AWS Bedrock Integration

This API uses AWS Bedrock with Claude 3 model for text summarisation. 

### Supported Models
- `anthropic.claude-3-sonnet-20240229-v1:0` (recommended - fast & cost-effective)
- `anthropic.claude-3-opus-20240229-v1:0` (most capable)
- `anthropic.claude-3-haiku-20240307-v1:0` (fastest & cheapest)

Change the model by updating `BEDROCK_MODEL_ID` in your `.env` file.

### API Key Requirements
- Must have Bedrock API access enabled in your AWS account
- Bearer token should have permissions for `bedrock:InvokeModel`

## Troubleshooting

### "AWS_BEARER_TOKEN_BEDROCK environment variable is required"
- Make sure you have created a `.env` file (copy from `.env.example`)
- Ensure the file contains a valid `AWS_BEARER_TOKEN_BEDROCK` value

### "Error invoking Bedrock model"
- Verify your AWS credentials are valid
- Check that Bedrock is available in your AWS region
- Ensure your token has necessary permissions
- Verify the model ID is correct

### Connection Refused
- Check if the API is running: `GET http://localhost:8000/health`
- Verify the port (default 8000) is not in use
- Check firewall settings if accessing from remote machine

## Performance Considerations

- **Token Limits**: Monitor input/output tokens returned in responses for cost tracking
- **Model Selection**: Use Haiku for speed, Sonnet for balance, Opus for quality
- **Timeout**: API requests may take 5-10 seconds depending on text length
- **Concurrency**: FastAPI handles multiple requests efficiently

## Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `AWS_BEARER_TOKEN_BEDROCK` | - | AWS short-term API key (required) |
| `AWS_REGION` | us-east-1 | AWS region for Bedrock |
| `BEDROCK_MODEL_ID` | anthropic.claude-3-sonnet-20240229-v1:0 | Claude model to use |
| `API_PORT` | 8000 | Port to run API on |
| `API_HOST` | 0.0.0.0 | Host to bind API to |

## License

MIT License

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review AWS Bedrock documentation
3. Check FastAPI documentation
4. Enable debug logging for more details

## Next Steps

1. ✅ Set up environment variables in `.env`
2. ✅ Install dependencies: `pip install -r requirements.txt`
3. ✅ Start the API: `python -m uvicorn src.main:app --reload`
4. ✅ Test endpoints using curl or Postman
5. ✅ Run tests: `pytest tests/ -v`
6. ✅ Deploy to production using Docker or your preferred platform
