#!/bin/bash

# Exit on error
set -e

echo "🚀 Setting up Work Production AI Agent..."

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.8.0"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then 
    echo "✅ Python version $python_version is compatible"
else
    echo "❌ Python version $python_version is not compatible. Please install Python 3.8 or higher"
    exit 1
fi

# Create virtual environment
echo "🔧 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file
echo "🔐 Setting up environment variables..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env file from template"
else
    echo "ℹ️ .env file already exists"
fi

# Initialize database
echo "🗄️ Setting up database..."
if command -v docker &> /dev/null; then
    echo "🐳 Starting PostgreSQL and Redis with Docker..."
    docker-compose up -d db redis
    
    # Wait for PostgreSQL to be ready
    echo "⏳ Waiting for PostgreSQL to be ready..."
    until docker-compose exec -T db pg_isready; do
        echo "PostgreSQL is unavailable - sleeping"
        sleep 1
    done
    
    echo "✅ Database services are running"
else
    echo "⚠️ Docker not found. Please ensure PostgreSQL and Redis are running locally"
fi

# Create database tables
echo "🏗️ Creating database tables..."
python -c "
from app.main import app
from app.models import Base
from app.database import engine
Base.metadata.create_all(bind=engine)
"

# Set up pre-commit hooks
echo "🔍 Setting up pre-commit hooks..."
if command -v pre-commit &> /dev/null; then
    pre-commit install
    echo "✅ Pre-commit hooks installed"
else
    echo "⚠️ pre-commit not found. Install with: pip install pre-commit"
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs
mkdir -p data

# Set up test environment
echo "🧪 Setting up test environment..."
python -m pytest --setup-only

echo """
✨ Setup completed! ✨

To start the application:
1. Update the .env file with your credentials
2. Run the development server:
   uvicorn app.main:app --reload

To run tests:
   python -m pytest

For production deployment:
1. Build the Docker image:
   docker build -t work-production-ai .
2. Deploy using docker-compose:
   docker-compose up -d
"""

# Make the script executable
chmod +x scripts/setup.sh
