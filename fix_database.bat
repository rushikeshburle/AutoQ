@echo off
echo Fixing database configuration...
cd backend

REM Backup existing .env
if exist .env (
    copy .env .env.backup
    echo Backed up .env to .env.backup
)

REM Update DATABASE_URL to use SQLite
powershell -Command "(Get-Content .env) -replace 'DATABASE_URL=postgresql://.*', 'DATABASE_URL=sqlite:///./autoq.db' | Set-Content .env"

echo.
echo ✓ Database configuration updated to use SQLite
echo.
echo You can now start the backend server again!
echo.
pause
