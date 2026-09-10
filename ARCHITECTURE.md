# Architecture & Design Documentation

## Project Overview

This is a production-ready FastAPI backend service for text Summarisation using AWS Bedrock. It's designed as a CDP (Customer Data Platform) microservice component.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Client Applications                      │
│                  (Web, Mobile, CDP, etc.)                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ HTTP/REST
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Application                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              API Layer (main.py)                     │  │
│  │  ┌─────────────┐  ┌────────────┐  ┌──────────────┐  │  │
│  │  │ /health     │  │ /config    │  │ /summarise   │  │  │
│  │  └─────────────┘  └────────────┘  └──────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
│                       │                                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           Data Validation Layer (models.py)          │  │
│  │  - SummariseRequest                                  │  │
│  │  - SummariseResponse                                 │  │
│  │  - ErrorResponse                                     │  │
│  └──────────────────────────────────────────────────────┘  │
│                       │                                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │      Business Logic Layer (bedrock_summarizer.py)    │  │
│  │  - BedrockSummariser class                           │  │
│  │  - Prompt formatting                                 │  │
│  │  - Response parsing                                  │  │
│  └──────────────────────────────────────────────────────┘  │
│                       │                                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │     Configuration Layer (config.py, auth.py)         │  │
│  │  - Environment variable management                   │  │
│  │  - Bearer token authentication                       │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ AWS SDK (boto3)
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  AWS Bedrock Runtime                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │          Claude 3 Model Inference                    │  │
│  │  - anthropic.claude-3-sonnet-20240229-v1:0           │  │
│  │  - Text Processing & Summarisation                   │  │
│  │  - Token counting & cost tracking                    │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Component Breakdown

### 1. **main.py - API Layer**
- **FastAPI Application**: RESTful API endpoints
- **CORS Middleware**: Cross-origin request support
- **Error Handling**: Standardized error responses
- **Endpoints**:
  - `GET /health`: Service health check
  - `GET /config`: Configuration display
  - `POST /summarise`: Main summarisation endpoint
  - `GET /docs`: Interactive Swagger documentation

### 2. **models.py - Data Validation**
- **Pydantic Models**: Type-safe request/response validation
- **SummariseRequest**: Input validation with constraints
  - `text` (required): Minimum 1 character
  - `max_length` (optional): 50-1000 words (default: 100)
- **SummariseResponse**: Structured output with metadata
  - Original text, summary, model ID
  - Token usage (input/output) for cost tracking
- **ErrorResponse**: Consistent error format

### 3. **bedrock_summarizer.py - Business Logic**
- **BedrockSummariser Class**: Core summarisation logic
- **AWS Bedrock Integration**: boto3 client initialization
- **Prompt Engineering**: Optimized prompts for Claude
- **Response Parsing**: Extract summary and token counts
- **Singleton Pattern**: Reusable instance across requests
- **Error Handling**: AWS-specific exception handling

### 4. **config.py - Configuration Management**
- **Settings Class**: Centralized configuration
- **Environment Variables**: Loaded from `.env` file
- **Validation**: Required values checked at startup
- **Variables**:
  - AWS credentials (bearer token)
  - AWS region
  - Model ID
  - API host/port

### 5. **auth.py - Authentication**
- **BearerTokenAuth Class**: Token verification
- **Short-term API Key Support**: For AWS authentication
- **Request Middleware**: Authorization header validation
- **Decorator Support**: Optional route-level auth

## Data Flow

### Request Flow (Summarisation Endpoint)

```
1. Client sends POST /summarise
   └─> { "text": "...", "max_length": 100 }

2. FastAPI validates request
   └─> Pydantic model validation

3. BedrockSummariser processes request
   ├─> Format prompt with text
   ├─> Invoke AWS Bedrock model
   └─> Parse response

4. Response returned to client
   └─> {
         "original_text": "...",
         "summary": "...",
         "input_tokens": 127,
         "output_tokens": 45,
         "model": "..."
       }
```

## Authentication Flow

### Bearer Token Authentication

```
1. Client adds Authorization header
   └─> Authorization: Bearer <short_term_api_key>

2. Middleware extracts token
   └─> Removes "Bearer " prefix

3. Token verified against environment
   └─> Compares with AWS_BEARER_TOKEN_BEDROCK

4. If valid → Request proceeds
   If invalid → 401 Unauthorized response
```

## AWS Bedrock Integration

### Model Selection
- **Claude 3 Sonnet** (recommended): Fast, cost-effective
- **Claude 3 Opus**: Most capable, slower
- **Claude 3 Haiku**: Fastest, cheapest

### Token Counting
- **Input tokens**: Number of tokens in the original text
- **Output tokens**: Number of tokens in the summary
- **Used for**: Cost estimation and monitoring

### Error Handling
```
AWS API Errors
    ├─> Authentication error → 401
    ├─> Rate limit exceeded → 429
    ├─> Invalid model → 400
    └─> Service error → 500
```

## Deployment Patterns

### 1. **Local Development**
```bash
python -m uvicorn src.main:app --reload
```

### 2. **Docker Container**
```bash
docker build -t summarisation-api .
docker run -p 8000:8000 --env-file .env summarisation-api
```

### 3. **Docker Compose**
```bash
docker-compose up
```

### 4. **Production Deployment**
- Use IAM roles instead of bearer tokens
- Deploy behind reverse proxy (nginx)
- Enable HTTPS/TLS
- Set up monitoring and logging
- Use container orchestration (Kubernetes, ECS)

## Performance Characteristics

### Latency
- **Average**: 2-5 seconds per request
- **Depends on**: Text length, AWS region, model selection

### Throughput
- **Concurrent requests**: Handled by FastAPI/Uvicorn
- **Default workers**: 1 (use `--workers N` for production)
- **Scalable**: Stateless design allows horizontal scaling

### Resource Usage
- **Memory**: ~200-300 MB base + model cache
- **CPU**: Depends on concurrency
- **Network**: Varies with text size and token count

## Security Considerations

### 1. **Authentication**
- Short-term bearer tokens (configured via environment)
- Not suitable for public APIs (recommended for internal use)

### 2. **Data Protection**
- HTTPS/TLS in production
- No data persistence by default
- Sensitive config in environment variables

### 3. **Access Control**
- CORS enabled for flexibility (restrict in production)
- Bearer token validation on requests
- Rate limiting recommended for production

### 4. **Input Validation**
- Pydantic validation on all inputs
- Text length constraints
- Parameter range checking

## Error Handling Strategy

### Client Errors (4xx)
```
400 Bad Request
├─> Invalid input format
├─> Text validation failed
└─> Parameter out of range

401 Unauthorized
└─> Invalid or missing bearer token

422 Unprocessable Entity
└─> Pydantic validation error
```

### Server Errors (5xx)
```
500 Internal Server Error
├─> AWS Bedrock service error
├─> Authentication failure
└─> Unexpected exception
```

## Testing Strategy

### Unit Tests
- Model validation tests
- Configuration tests
- Prompt formatting tests

### Integration Tests
- Full endpoint tests
- Mocked Bedrock responses
- Error handling verification

### Manual Testing
- `test_client.py`: Interactive test suite
- `examples.py`: Real-world usage patterns
- API docs: `/docs` endpoint

## Extension Points

### 1. **Add New Endpoints**
```python
@app.post("/batch-summarise")
async def batch_summarise(requests: List[SummariseRequest]):
    # Batch processing logic
    pass
```

### 2. **Add Caching**
```python
from functools import lru_cache
# Cache frequently summarised texts
```

### 3. **Add Database**
```python
# Store summaries, audit logs
# Use SQLAlchemy with async support
```

### 4. **Add Monitoring**
```python
from prometheus_client import Counter, Histogram
# Track requests, latency, errors
```

## Development Workflow

```
1. Clone/Download project
   ↓
2. Create virtual environment
   ↓
3. Install dependencies: pip install -r requirements.txt
   ↓
4. Configure .env with AWS credentials
   ↓
5. Start API: python -m uvicorn src.main:app --reload
   ↓
6. Test endpoints: python test_client.py
   ↓
7. Run test suite: pytest tests/ -v
   ↓
8. Make changes → Auto-reload → Test
```

## Dependencies

### Core
- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation
- **boto3**: AWS SDK
- **python-dotenv**: Environment configuration

### Testing
- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting

### Optional (Production)
- **Docker**: Containerization
- **Gunicorn**: WSGI server
- **Nginx**: Reverse proxy

## File Structure

```
summarise-data-llm/
├── src/                          # Application code
│   ├── __init__.py
│   ├── main.py                   # FastAPI app & routes
│   ├── config.py                 # Configuration
│   ├── models.py                 # Pydantic models
│   ├── bedrock_summarizer.py     # Core logic
│   └── auth.py                   # Authentication
├── tests/                        # Test suite
│   ├── __init__.py
│   └── test_api.py
├── requirements.txt              # Python dependencies
├── pyproject.toml                # Project metadata
├── pytest.ini                    # Pytest config
├── conftest.py                   # Pytest fixtures
├── .env                          # Runtime config (local)
├── .env.example                  # Config template
├── .gitignore                    # Git ignore rules
├── README.md                     # Full documentation
├── QUICK_START.md                # Quick setup guide
├── ARCHITECTURE.md               # This file
├── Dockerfile                    # Container image
├── docker-compose.yml            # Docker setup
├── test_client.py                # Interactive tests
├── examples.py                   # Usage examples
├── tasks.py                      # Task runner
├── setup.sh                      # Linux/Mac setup
└── setup.bat                     # Windows setup
```

## Troubleshooting Guide

### Issue: "Module not found"
- Check virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### Issue: "AWS credentials not found"
- Verify `.env` file exists
- Check `AWS_BEARER_TOKEN_BEDROCK` is set
- Restart API after editing `.env`

### Issue: "Connection refused"
- Verify API is running on correct port
- Check firewall settings
- Try different port if 8000 is in use

### Issue: "Token validation failed"
- Verify bearer token format: `Authorization: Bearer <token>`
- Check token hasn't expired
- Verify token matches `AWS_BEARER_TOKEN_BEDROCK`

## Future Enhancements

1. **Streaming Responses**: Support large text with streaming
2. **Caching Layer**: Redis for frequently summarised texts
3. **Batch Processing**: Queue-based bulk Summarisation
4. **Analytics Dashboard**: Track usage and costs
5. **Model Selection UI**: Allow runtime model changes
6. **Custom Prompts**: User-defined Summarisation instructions
7. **Multi-language Support**: Summarisation in different languages
8. **Sentiment Analysis**: Combined with Summarisation
9. **Source Attribution**: Track source documents in summaries
10. **A/B Testing**: Compare different model outputs

## Contributing

When extending this project:
1. Follow existing code structure
2. Add tests for new features
3. Update documentation
4. Follow PEP 8 style guide
5. Use type hints for functions

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
