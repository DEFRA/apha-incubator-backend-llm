@echo off
REM Quick start script for the Text Summarization API (Windows)

echo ================================
echo Text Summarization API - Setup
echo ================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    exit /b 1
)

echo Python found: 
python --version

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo.
    echo Creating .env file...
    copy .env.example .env
    echo WARNING: Please edit .env and add your AWS credentials:
    echo   - AWS_BEARER_TOKEN_BEDROCK: Your short-term API key
)

echo.
echo ================================
echo Setup complete!
echo ================================
echo.
echo Next steps:
echo 1. Edit .env file with your AWS credentials
echo 2. Start the API: python -m uvicorn src.main:app --reload
echo 3. In another terminal, run: python test_client.py
echo 4. Visit http://localhost:8000/docs for interactive API documentation
echo.
pause
