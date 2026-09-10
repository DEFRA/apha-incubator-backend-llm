# Quick Start Guide - Text Summarisation API

Get your text summarisation API running in 5 minutes!

## 1️⃣ Prerequisites

- Python 3.8 or higher
- AWS account with Bedrock access
- Short-term AWS API key (bearer token)

## 2️⃣ Clone/Download the Project

You already have the project folder ready at:
```
c:\Users\da000087\OneDrive - Defra\AI\summarise-data-llm
```

## 3️⃣ Set Up Environment (Windows)

### Option A: Use Batch Script (Easiest)
```bash
cd "c:\Users\da000087\OneDrive - Defra\AI\summarise-data-llm"
setup.bat
```

### Option B: Manual Setup
```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 4️⃣ Configure AWS Credentials

Edit the `.env` file and replace:
```env
AWS_BEARER_TOKEN_BEDROCK=your_actual_api_key_here
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
API_PORT=8000
API_HOST=0.0.0.0
```

⚠️ **IMPORTANT:** Never commit your `.env` file to git. It's in `.gitignore` for protection.

## 5️⃣ Start the API

```bash
# With live reload (development)
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Or use the task runner
python tasks.py dev
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

## 6️⃣ Test the API

Open a new terminal (with venv activated):

### Option A: Use the Test Client
```bash
python test_client.py
```

### Option B: Use curl
```bash
# Health check
curl http://localhost:8000/health

# Summarise text
curl -X POST http://localhost:8000/summarise \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your text here...",
    "max_length": 100
  }'
```

### Option C: Interactive API Docs
Visit: http://localhost:8000/docs (Swagger UI)
or: http://localhost:8000/redoc (ReDoc)

## 7️⃣ Common Tasks

### Run Tests
```bash
pytest tests/ -v
```

### Run Examples
```bash
python examples.py
```

### View Token Usage
The API response includes `input_tokens` and `output_tokens` for cost tracking:
```json
{
  "summary": "...",
  "input_tokens": 127,
  "output_tokens": 45,
  "model": "anthropic.claude-3-sonnet-20240229-v1:0"
}
```

## 🐳 Docker Deployment

```bash
# Build and run with Docker
docker-compose up --build

# API will be at http://localhost:8000
```

## 📊 API Endpoints Quick Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Check API status |
| `/config` | GET | View configuration |
| `/summarise` | POST | Summarise text |
| `/docs` | GET | Interactive documentation |

## ✅ Verification Checklist

- [ ] Python installed (check: `python --version`)
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip list | grep fastapi`)
- [ ] `.env` file configured with AWS credentials
- [ ] API running without errors
- [ ] Health check responds: `http://localhost:8000/health`
- [ ] Can successfully summarise text

## 🐛 Troubleshooting

### "AWS_BEARER_TOKEN_BEDROCK not found"
- Check `.env` file exists in project root
- Verify the variable is uncommented and has a value
- Restart the API after editing `.env`

### "Connection refused on port 8000"
- Port 8000 might be in use
- Change port: `API_PORT=8001` in `.env`
- Or kill the process: `netstat -ano | findstr :8000`

### "Module not found" errors
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python version: `python --version` (needs 3.8+)

### AWS Authentication Errors
- Verify bearer token is correct in `.env`
- Check AWS region is supported for Bedrock
- Ensure your AWS account has Bedrock access enabled

## 📚 Next Steps

1. Read [README.md](README.md) for detailed documentation
2. Check [examples.py](examples.py) for integration patterns
3. Review [tests/test_api.py](tests/test_api.py) for test examples
4. Deploy to production (see Docker section)

## 🚀 Production Deployment

For production use:
1. Use environment-specific `.env` files
2. Set `API_HOST=127.0.0.1` and use a reverse proxy (nginx, etc.)
3. Enable HTTPS/TLS
4. Use AWS IAM roles instead of bearer tokens
5. Add request rate limiting
6. Set up monitoring and logging
7. Use Docker for containerization
8. Deploy to ECS, Lambda, or your preferred platform

## 💡 Tips

- Use `max_length=50-100` for most use cases
- Monitor token usage for cost optimization
- Batch process multiple texts for efficiency
- Use health check for service monitoring
- Check API documentation at `/docs` while running

## 📞 Support

For issues:
1. Check the troubleshooting section above
2. Review AWS Bedrock documentation
3. Check FastAPI documentation
4. Enable debug mode and check logs

---

**You're all set! Happy summarising! 🎉**
