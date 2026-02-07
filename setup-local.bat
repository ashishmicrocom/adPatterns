@echo off
REM AdPatterns Local Setup Script for Windows
REM This script helps you set up the project for local development

echo.
echo ================================
echo 🚀 AdPatterns Local Setup
echo ================================
echo.

REM Check if CSV model file exists
echo 📊 Checking for model data...
if exist "adpattern_final_production.csv" (
    echo ✓ Model CSV file found
) else (
    echo ✗ Model CSV file not found!
    echo    Please ensure 'adpattern_final_production.csv' is in the root directory
    exit /b 1
)

echo.
echo 🔧 Setting up Backend...
cd backend

REM Check if .env exists
if not exist ".env" (
    echo ⚠ Creating .env from template...
    copy .env.example .env
    echo → Please edit backend\.env with your MongoDB URL and SECRET_KEY
) else (
    echo ✓ .env file exists
)

REM Install Python dependencies
echo 📦 Installing Python dependencies...
where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    pip install -r requirements.txt
    echo ✓ Python dependencies installed
) else (
    echo ✗ Python not found! Please install Python 3.11+
    exit /b 1
)

cd ..
echo.
echo 🎨 Setting up Frontend...
cd frontend

REM Check if .env.local exists
if not exist ".env.local" (
    echo ⚠ Creating .env.local from template...
    copy .env.local.example .env.local
    echo ✓ .env.local created with default values
) else (
    echo ✓ .env.local file exists
)

REM Install Node dependencies
echo 📦 Installing Node dependencies...
where npm >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    call npm install
    echo ✓ Node dependencies installed
) else (
    echo ✗ npm not found! Please install Node.js 18+
    exit /b 1
)

cd ..
echo.
echo ================================
echo ✅ Setup Complete!
echo ================================
echo.
echo 📝 Next Steps:
echo 1. Edit backend\.env with your MongoDB credentials
echo 2. Generate a SECRET_KEY: python -c "import secrets; print(secrets.token_urlsafe(32))"
echo.
echo 🏃 To run the application:
echo.
echo Terminal 1 (Backend):
echo   cd backend
echo   uvicorn app.main:app --reload
echo.
echo Terminal 2 (Frontend):
echo   cd frontend
echo   npm run dev
echo.
echo Then open: http://localhost:3000
echo.
pause
