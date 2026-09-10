#!/bin/bash
# Quick start script for the Text Summarisation API

echo "================================"
echo "Text Summarisation API - Setup"
echo "================================"

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed"
    exit 1
fi

echo "✓ Python found: $(python --version)"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate  # For Linux/Mac
# For Windows, use: venv\Scripts\activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file..."
    cp .env.example .env
    echo "⚠ Please edit .env and add your AWS credentials:"
    echo "  - AWS_BEARER_TOKEN_BEDROCK: Your short-term API key"
fi

echo ""
echo "================================"
echo "Setup complete!"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your AWS credentials"
echo "2. Start the API: python -m uvicorn src.main:app --reload"
echo "3. In another terminal, run: python test_client.py"
echo "4. Visit http://localhost:8000/docs for interactive API documentation"
