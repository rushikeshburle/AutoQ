@echo off
echo Starting AutoQ Backend Server...
echo.
cd backend
call venv\Scripts\activate.bat
echo Virtual environment activated
echo.
echo Starting uvicorn server on http://127.0.0.1:8000
echo Press Ctrl+C to stop the server
echo.
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
pause
