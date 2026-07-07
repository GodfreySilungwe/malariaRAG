#!/bin/bash
# Script to run tests for MalariaAI RAG

set -e

echo "🧪 Running MalariaAI RAG Tests"
echo "=============================="

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if venv exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found. Creating one...${NC}"
    python -m venv venv
fi

# Activate venv
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt
pip install -q pytest pytest-cov pytest-timeout flake8 black

# Run linting
echo -e "${YELLOW}\n🔍 Running linting (flake8)...${NC}"
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics || true
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics || true

# Run tests
echo -e "${YELLOW}\n🧪 Running pytest...${NC}"
pytest tests/ -v --cov=. --cov-report=html --cov-report=term --tb=short

# Check coverage
COVERAGE=$(grep -oP 'TOTAL\s+\K[0-9]+(?=%)' .coverage.json 2>/dev/null || echo "N/A")

# Summary
echo -e "\n${GREEN}✅ All tests completed!${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "Coverage report: ${COVERAGE}"
echo "Detailed report: htmlcov/index.html"
echo -e "${GREEN}✅ Ready for deployment!${NC}"

deactivate
