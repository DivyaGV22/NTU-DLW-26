# Quick Start Guide

## Step 1: Backend Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the API server (from project root):
```bash
cd backend
python -m uvicorn api.main:app --reload
```

Or from project root:
```bash
python -m uvicorn backend.api.main:app --reload
```

3. Verify the API is running:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

4. (Optional) Generate sample data:
```bash
cd backend
python utils/sample_data.py
```

## Step 2: Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Open the dashboard:
- http://localhost:3000

## Step 3: Using the System

1. **Create a Student**: Click "+ New Student" and enter name and email
2. **Record Activities**: Use the "Record Learning Activity" form to log study sessions, quizzes, etc.
3. **View Analytics**: See your learning state, progress charts, and topic proficiencies
4. **Get Recommendations**: Check the recommendations panel for personalized guidance
5. **Understand Insights**: Click the "+" button on recommendations to see detailed explanations

## Troubleshooting

### Backend Issues
- **Import errors**: Make sure you're running from the `backend` directory or have the correct Python path
- **Database errors**: The SQLite database will be created automatically on first run
- **Port already in use**: Change the port with `--port 8001`

### Frontend Issues
- **API connection errors**: Ensure the backend is running on port 8000
- **CORS errors**: Check that the backend CORS settings include your frontend URL
- **Module not found**: Run `npm install` again

## Next Steps

- Explore the API documentation at http://localhost:8000/docs
- Try recording different types of learning interactions
- Observe how recommendations change based on your activity
- Check how the learning state evolves over time

