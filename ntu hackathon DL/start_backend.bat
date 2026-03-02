@echo off
echo Starting Learning Analytics Backend...
cd backend
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
pause

