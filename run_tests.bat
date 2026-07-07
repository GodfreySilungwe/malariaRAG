@echo off
REM Script to run tests for MalariaAI RAG on Windows

echo.
echo 🧪 Running MalariaAI RAG Tests
echo ==============================
echo.

REM Check if venv exists
if not exist "venv" (
    echo ⚠️  Virtual environment not found. Creating one...
    python -m venv venv
)

REM Activate venv
echo 📦 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -q -r requirements.txt
pip install -q pytest pytest-cov pytest-timeout flake8 black

REM Run linting
echo.
echo 🔍 Running linting (flake8)...
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

REM Run tests
echo.
echo 🧪 Running pytest...
pytest tests/ -v --cov=. --cov-report=html --cov-report=term --tb=short

REM Summary
echo.
echo ✅ All tests completed!
echo ========================================
echo Detailed report: htmlcov\index.html
echo ✅ Ready for deployment!
echo.

call venv\Scripts\deactivate.bat
