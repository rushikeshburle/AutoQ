Write-Host "Starting AutoQ Backend Server..." -ForegroundColor Green
Write-Host ""
Set-Location backend
& .\venv\Scripts\Activate.ps1
Write-Host "Virtual environment activated" -ForegroundColor Yellow
Write-Host ""
Write-Host "Starting uvicorn server on http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
