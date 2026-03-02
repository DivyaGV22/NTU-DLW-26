@echo off
echo Starting Backend Server...
echo.
cd backend
python -m uvicorn api.main:app --reload
pause

