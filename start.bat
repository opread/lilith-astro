@echo off
echo Starting Lilith Application...

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Start the backend server in background
start "Backend Server" cmd /k "uvicorn src.interfaces.api.main:app --reload --host 0.0.0.0 --port 8000"

REM Wait a moment for backend to start
timeout /t 2 /nobreak > nul

REM Start the frontend
cd frontend
start "Frontend" cmd /k "npm start"

echo Applications started!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000