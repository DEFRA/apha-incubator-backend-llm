FROM python:3.11-slim

WORKDIR /app

# curl is required for the CDP platform healthcheck
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ src/

# CDP injects PORT=8085 at runtime; default kept for local docker use
ENV PORT=8000
EXPOSE $PORT

# CDP's platform healthcheck expects curl against $PORT/health
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/health || exit 1

# Start the application, binding to the CDP-provided PORT
CMD ["sh", "-c", "python -m uvicorn src.main:app --host 0.0.0.0 --port ${PORT}"]
