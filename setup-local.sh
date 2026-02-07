#!/bin/bash

# AdPatterns Local Setup Script
# This script helps you set up the project for local development

echo "🚀 AdPatterns Local Setup"
echo "=========================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if CSV model file exists
echo "📊 Checking for model data..."
if [ -f "adpattern_final_production.csv" ]; then
    echo -e "${GREEN}✓${NC} Model CSV file found"
else
    echo -e "${RED}✗${NC} Model CSV file not found!"
    echo "   Please ensure 'adpattern_final_production.csv' is in the root directory"
    exit 1
fi

echo ""
echo "🔧 Setting up Backend..."
cd backend

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠${NC} Creating .env from template..."
    cp .env.example .env
    echo -e "${YELLOW}→${NC} Please edit backend/.env with your MongoDB URL and SECRET_KEY"
else
    echo -e "${GREEN}✓${NC} .env file exists"
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
if command -v python3 &> /dev/null; then
    pip install -r requirements.txt
    echo -e "${GREEN}✓${NC} Python dependencies installed"
else
    echo -e "${RED}✗${NC} Python3 not found! Please install Python 3.11+"
    exit 1
fi

cd ..
echo ""
echo "🎨 Setting up Frontend..."
cd frontend

# Check if .env.local exists
if [ ! -f ".env.local" ]; then
    echo -e "${YELLOW}⚠${NC} Creating .env.local from template..."
    cp .env.local.example .env.local
    echo -e "${GREEN}✓${NC} .env.local created with default values"
else
    echo -e "${GREEN}✓${NC} .env.local file exists"
fi

# Install Node dependencies
echo "📦 Installing Node dependencies..."
if command -v npm &> /dev/null; then
    npm install
    echo -e "${GREEN}✓${NC} Node dependencies installed"
else
    echo -e "${RED}✗${NC} npm not found! Please install Node.js 18+"
    exit 1
fi

cd ..
echo ""
echo "✅ Setup Complete!"
echo ""
echo "📝 Next Steps:"
echo "1. Edit backend/.env with your MongoDB credentials"
echo "2. Generate a SECRET_KEY: python -c \"import secrets; print(secrets.token_urlsafe(32))\""
echo ""
echo "🏃 To run the application:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend"
echo "  uvicorn app.main:app --reload"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Then open: http://localhost:3000"
echo ""
