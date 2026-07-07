#!/bin/bash
# Setup script for MalariaAI RAG development environment

set -e

echo "🚀 Setting up MalariaAI RAG Development Environment"
echo "=================================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check Python version
echo "📦 Checking Python version..."
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
echo "Python version: $PYTHON_VERSION"

if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.10+"
    exit 1
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 Creating virtual environment...${NC}"
    python -m venv venv
else
    echo -e "${GREEN}✅ Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📥 Upgrading pip..."
pip install --upgrade pip setuptools wheel > /dev/null

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please update .env with your configuration${NC}"
fi

# Ingest corpus
if [ ! -d "chromadb" ] || [ -z "$(ls -A chromadb)" ]; then
    echo "📚 Ingesting corpus..."
    python ingest.py --data ./corpus --persist ./chromadb
else
    echo -e "${GREEN}✅ ChromaDB already exists${NC}"
fi

# Create test directories if needed
mkdir -p tests

echo ""
echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Run tests: ./run_tests.sh"
echo "2. Start API: python app.py"
echo "3. Start UI: streamlit run ui.py"
echo ""
echo "To deactivate the virtual environment later, run: deactivate"
