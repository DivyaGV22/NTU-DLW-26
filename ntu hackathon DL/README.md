# AI-Powered Learning Analytics & Recommendation System

An intelligent system that models a student's evolving learning state and provides personalized, actionable guidance to improve learning outcomes.

## Features

- **Learning State Modeling**: Tracks and models student learning interactions over time
- **Personalized Recommendations**: AI-generated insights tailored to each student's learning patterns
- **Explainable AI**: Clear explanations for why recommendations are made
- **Adaptive Learning**: Handles long-term changes including inactivity and accelerated progress
- **Interactive Dashboard**: Visual analytics and actionable insights

## Architecture

- **Backend**: Python with FastAPI, scikit-learn, pandas
- **Frontend**: React with modern UI components
- **ML Models**: Learning state prediction, recommendation generation, anomaly detection
- **Database**: SQLite for development (easily upgradeable to PostgreSQL)

## Project Structure

```
├── backend/
│   ├── models/          # ML models and data processing
│   ├── api/             # FastAPI endpoints
│   ├── database/        # Database models and migrations
│   └── utils/           # Utility functions
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/       # Dashboard pages
│   │   └── services/    # API services
├── data/                # Sample data and models
└── requirements.txt     # Python dependencies
```

## Quick Start

**New to the project?** See **[GETTING_STARTED.md](GETTING_STARTED.md)** for detailed step-by-step instructions!

### Quick Setup (TL;DR)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   cd frontend && npm install
   ```

2. **Start backend** (Terminal 1):
   ```bash
   cd backend
   python -m uvicorn api.main:app --reload
   ```
   → API: http://localhost:8000 | Docs: http://localhost:8000/docs

3. **Start frontend** (Terminal 2):
   ```bash
   cd frontend
   npm run dev
   ```
   → Dashboard: http://localhost:3000

4. **(Optional) Generate sample data:**
   ```bash
   cd backend
   python utils/sample_data.py
   ```

### Prerequisites
- Python 3.8+
- Node.js 16+ and npm
- pip (Python package manager)

## Usage

1. **Create a Student**: Use the dashboard to create a new student profile
2. **Record Interactions**: Track learning activities (study sessions, quizzes, assignments, etc.)
3. **View Learning State**: Monitor proficiency, engagement, and learning velocity
4. **Get Recommendations**: Receive AI-powered, personalized learning guidance
5. **Understand Insights**: View explainable reasoning for each recommendation
6. **Take Action**: Mark recommendations as viewed or completed

## Key Features Explained

### Learning State Modeling
- **Overall Proficiency**: Aggregated performance across all topics
- **Engagement Level**: Measures active participation and consistency
- **Learning Velocity**: Rate of improvement over time
- **Consistency Score**: Regularity of study patterns
- **Risk Assessment**: Identifies students at risk of falling behind

### Recommendation Types
- **Study**: Encourages regular learning activities
- **Practice**: Focuses on weak topics
- **Review**: Spaced repetition for better retention
- **Break**: Prevents burnout and maintains engagement
- **Accelerate**: Challenges high-performing students

### Explainable AI
Each recommendation includes:
- **Reasoning**: Clear explanation of why the recommendation was made
- **Supporting Data**: Evidence-based metrics and statistics
- **Action Items**: Step-by-step guidance for implementation

### Adaptive Learning
- **Inactivity Detection**: Identifies and addresses learning gaps
- **Accelerated Progress**: Recognizes fast learners and suggests advanced content
- **Long-term Tracking**: Adapts to changing learning patterns over time

