"""
FastAPI main application with endpoints for learning analytics
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import pandas as pd
import json

from database.models import (
    Base, get_db, Student, LearningInteraction, LearningState, Recommendation
)
from models.learning_state_model import LearningStateModel
from models.recommendation_engine import RecommendationEngine
from api.schemas import (
    StudentCreate, StudentResponse,
    InteractionCreate, InteractionResponse,
    LearningStateResponse,
    RecommendationResponse,
    DashboardData
)

app = FastAPI(title="Learning Analytics API", version="1.0.0")

# CORS middleware - Enhanced configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173", 
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://localhost:3000/",
        "http://127.0.0.1:3000/"
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Add CORS headers manually as backup (must be before routes)
@app.middleware("http")
async def add_cors_header(request, call_next):
    # Handle preflight OPTIONS requests
    if request.method == "OPTIONS":
        response = JSONResponse(content={})
        origin = request.headers.get("origin", "*")
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
        response.headers["Access-Control-Allow-Headers"] = "*"
        return response
    
    # Handle actual requests
    response = await call_next(request)
    origin = request.headers.get("origin", "*")
    if origin in ["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173"]:
        response.headers["Access-Control-Allow-Origin"] = origin
    else:
        response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

# Initialize ML models
state_model = LearningStateModel()
# Pass BKT model to recommendation engine for enhanced features
recommendation_engine = RecommendationEngine(bkt_model=state_model.bkt)


@app.get("/")
async def root():
    return {"message": "Learning Analytics API", "version": "1.0.0"}


@app.post("/students", response_model=StudentResponse)
async def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    """Create a new student"""
    db_student = Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@app.get("/students", response_model=List[StudentResponse])
async def get_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all students"""
    students = db.query(Student).offset(skip).limit(limit).all()
    return students


@app.get("/students/{student_id}", response_model=StudentResponse)
async def get_student(student_id: int, db: Session = Depends(get_db)):
    """Get a specific student"""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.post("/students/{student_id}/interactions", response_model=InteractionResponse)
async def create_interaction(
    student_id: int,
    interaction: InteractionCreate,
    db: Session = Depends(get_db)
):
    """Record a learning interaction"""
    # Verify student exists
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Create interaction (map metadata -> extra_data for DB)
    payload = interaction.dict()
    if "metadata" in payload:
        payload["extra_data"] = payload.pop("metadata")

    db_interaction = LearningInteraction(
        student_id=student_id,
        **payload
    )
    db.add(db_interaction)
    db.commit()
    db.refresh(db_interaction)
    
    # Update learning state
    await update_learning_state(student_id, db)
    
    return db_interaction


@app.get("/students/{student_id}/interactions", response_model=List[InteractionResponse])
async def get_interactions(
    student_id: int,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get interactions for a student"""
    interactions = db.query(LearningInteraction).filter(
        LearningInteraction.student_id == student_id
    ).order_by(LearningInteraction.timestamp.desc()).limit(limit).all()
    return interactions


@app.get("/students/{student_id}/state", response_model=LearningStateResponse)
async def get_learning_state(student_id: int, db: Session = Depends(get_db)):
    """Get current learning state for a student"""
    # Get latest state from database
    latest_state = db.query(LearningState).filter(
        LearningState.student_id == student_id
    ).order_by(LearningState.timestamp.desc()).first()
    
    if latest_state:
        return latest_state
    
    # If no state exists, compute it
    await update_learning_state(student_id, db)
    latest_state = db.query(LearningState).filter(
        LearningState.student_id == student_id
    ).order_by(LearningState.timestamp.desc()).first()
    
    if not latest_state:
        raise HTTPException(status_code=404, detail="Could not compute learning state")
    
    return latest_state


async def update_learning_state(student_id: int, db: Session):
    """Update learning state for a student"""
    # Get all interactions
    interactions = db.query(LearningInteraction).filter(
        LearningInteraction.student_id == student_id
    ).all()
    
    if not interactions:
        return
    
    # Convert to DataFrame
    interactions_data = [{
        'interaction_type': i.interaction_type,
        'topic': i.topic,
        'duration_minutes': i.duration_minutes,
        'score': i.score,
        'difficulty_level': i.difficulty_level,
        'engagement_score': i.engagement_score,
        'timestamp': i.timestamp
    } for i in interactions]
    
    interactions_df = pd.DataFrame(interactions_data)
    
    # Predict state
    state_dict = state_model.predict_state(interactions_df)
    
    # Extract topic proficiencies safely
    topic_profs = state_dict.get('topic_proficiencies', {})
    if not isinstance(topic_profs, dict):
        topic_profs = {}
    topic_profs_json = json.dumps(topic_profs)
    
    # Save to database (only include valid database fields)
    db_state = LearningState(
        student_id=student_id,
        overall_proficiency=state_dict.get('overall_proficiency', 0.5),
        engagement_level=state_dict.get('engagement_level', 0.5),
        learning_velocity=state_dict.get('learning_velocity', 0.0),
        consistency_score=state_dict.get('consistency_score', 0.5),
        days_since_last_activity=state_dict.get('days_since_last_activity', 0),
        is_active=state_dict.get('is_active', True),
        risk_level=state_dict.get('risk_level', 'medium'),
        topic_proficiencies=topic_profs_json
    )
    db.add(db_state)
    db.commit()


@app.get("/students/{student_id}/recommendations", response_model=List[RecommendationResponse])
async def get_recommendations(
    student_id: int,
    limit: int = 5,
    db: Session = Depends(get_db)
):
    """Get personalized recommendations for a student"""
    # Get learning state
    state = await get_learning_state(student_id, db)
    
    # Get interactions
    interactions = db.query(LearningInteraction).filter(
        LearningInteraction.student_id == student_id
    ).all()
    
    if not interactions:
        return []
    
    # Convert to DataFrame
    interactions_data = [{
        'interaction_type': i.interaction_type,
        'topic': i.topic,
        'duration_minutes': i.duration_minutes,
        'score': i.score,
        'difficulty_level': i.difficulty_level,
        'engagement_score': i.engagement_score,
        'timestamp': i.timestamp
    } for i in interactions]
    
    interactions_df = pd.DataFrame(interactions_data)
    
    # Prepare state dict
    topic_proficiencies = json.loads(state.topic_proficiencies) if state.topic_proficiencies else {}
    
    # Get BKT mastery from state model (safely)
    bkt_mastery = {}
    try:
        for topic in topic_proficiencies.keys():
            bkt_mastery[topic] = state_model.bkt.get_mastery(topic)
    except Exception as e:
        # If BKT fails, use regular proficiencies
        bkt_mastery = topic_proficiencies
    
    state_dict = {
        'overall_proficiency': state.overall_proficiency,
        'engagement_level': state.engagement_level,
        'learning_velocity': state.learning_velocity,
        'consistency_score': state.consistency_score,
        'days_since_last_activity': state.days_since_last_activity,
        'is_active': state.is_active,
        'risk_level': state.risk_level,
        'topic_proficiencies': topic_proficiencies,
        'bkt_mastery': bkt_mastery,
        'burnout_risk': 'low',  # Default if not available
        'burnout_signals': []
    }
    
    # Get recent interactions (last 30 days)
    cutoff = datetime.now() - timedelta(days=30)
    recent_df = interactions_df[pd.to_datetime(interactions_df['timestamp']) >= cutoff]
    
    # Generate recommendations
    recommendations = recommendation_engine.generate_recommendations(
        state_dict,
        recent_df,
        interactions_df
    )
    
    # Save recommendations to database
    db_recommendations = []
    for rec in recommendations[:limit]:
        # Check if similar recommendation already exists
        existing = db.query(Recommendation).filter(
            Recommendation.student_id == student_id,
            Recommendation.title == rec['title'],
            Recommendation.status == 'pending'
        ).first()
        
        if not existing:
            db_rec = Recommendation(
                student_id=student_id,
                **rec
            )
            db.add(db_rec)
            db_recommendations.append(db_rec)
    
    db.commit()
    
    # Return all pending recommendations
    pending_recs = db.query(Recommendation).filter(
        Recommendation.student_id == student_id,
        Recommendation.status == 'pending'
    ).order_by(Recommendation.created_at.desc()).limit(limit).all()
    
    return pending_recs


@app.put("/recommendations/{recommendation_id}/status")
async def update_recommendation_status(
    recommendation_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    """Update recommendation status"""
    rec = db.query(Recommendation).filter(Recommendation.id == recommendation_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    
    rec.status = status
    if status == 'viewed':
        rec.viewed_at = datetime.utcnow()
    elif status == 'completed':
        rec.completed_at = datetime.utcnow()
    
    db.commit()
    return {"message": "Status updated", "status": status}


@app.get("/students/{student_id}/dashboard", response_model=DashboardData)
async def get_dashboard_data(student_id: int, db: Session = Depends(get_db)):
    """Get comprehensive dashboard data"""
    try:
        # Get student
        student = await get_student(student_id, db)
        
        # Get state
        state = await get_learning_state(student_id, db)
        
        # Get interactions
        interactions = await get_interactions(student_id, limit=100, db=db)
        
        # Get recommendations
        recommendations = await get_recommendations(student_id, limit=5, db=db)
        
        # Calculate additional metrics safely
        total_study_time = sum(i.duration_minutes for i in interactions if i.duration_minutes) or 0
        scores = [i.score for i in interactions if i.score is not None]
        avg_score = sum(scores) / len(scores) if scores else 0.0
        
        return {
            "student": student,
            "learning_state": state,
            "interactions": interactions,
            "recommendations": recommendations,
            "metrics": {
                "total_interactions": len(interactions),
                "total_study_time": total_study_time,
                "avg_score": avg_score
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        # Log error and return a proper error response
        import traceback
        print(f"Dashboard error: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error loading dashboard: {str(e)}")


@app.get("/students/{student_id}/study-plan/{time_minutes}")
async def get_study_plan(
    student_id: int,
    time_minutes: int,
    db: Session = Depends(get_db)
):
    """Get ROI-optimized study plan for given time budget"""
    from models.study_roi_optimizer import StudyROIOptimizer
    
    # Get learning state
    state = await get_learning_state(student_id, db)
    
    # Get interactions to update BKT
    interactions = db.query(LearningInteraction).filter(
        LearningInteraction.student_id == student_id
    ).all()
    
    if interactions:
        interactions_data = [{
            'interaction_type': i.interaction_type,
            'topic': i.topic,
            'duration_minutes': i.duration_minutes,
            'score': i.score,
            'difficulty_level': i.difficulty_level,
            'engagement_score': i.engagement_score,
            'timestamp': i.timestamp
        } for i in interactions]
        
        interactions_df = pd.DataFrame(interactions_data)
        # Update BKT models
        state_model.predict_state(interactions_df)
    
    # Get topic masteries
    topic_proficiencies = json.loads(state.topic_proficiencies) if state.topic_proficiencies else {}
    bkt_mastery = {}
    for topic in topic_proficiencies.keys():
        bkt_mastery[topic] = state_model.bkt.get_mastery(topic)
    
    if not bkt_mastery:
        return {"error": "No topic data available"}
    
    # Generate study plan
    roi_optimizer = StudyROIOptimizer(state_model.bkt)
    study_plan = roi_optimizer.generate_study_plan(
        time_minutes,
        bkt_mastery
    )
    
    return study_plan


@app.get("/students/{student_id}/learning-twin/predict/{topic}")
async def predict_retention(
    student_id: int,
    topic: str,
    days: int = 7,
    db: Session = Depends(get_db)
):
    """Predict retention decay for a topic using Learning Twin"""
    from models.learning_twin import DigitalLearningTwin
    
    # Get interactions to ensure BKT is updated
    interactions = db.query(LearningInteraction).filter(
        LearningInteraction.student_id == student_id,
        LearningInteraction.topic == topic
    ).all()
    
    if interactions:
        interactions_data = [{
            'interaction_type': i.interaction_type,
            'topic': i.topic,
            'score': i.score,
            'timestamp': i.timestamp
        } for i in interactions]
        
        interactions_df = pd.DataFrame(interactions_data)
        for _, row in interactions_df.iterrows():
            is_correct = row.get('score', 0) >= 0.5
            timestamp = pd.to_datetime(row.get('timestamp', datetime.now()))
            state_model.bkt.update_mastery(topic, is_correct, timestamp)
    
    # Predict retention
    learning_twin = DigitalLearningTwin(state_model.bkt)
    prediction = learning_twin.predict_retention_decay(topic, days)
    
    return prediction


@app.get("/students/{student_id}/mistake-analysis")
async def get_mistake_analysis(
    student_id: int,
    db: Session = Depends(get_db)
):
    """Get mistake intelligence analysis"""
    # Get interactions
    interactions = db.query(LearningInteraction).filter(
        LearningInteraction.student_id == student_id
    ).all()
    
    if not interactions:
        return {"error": "No interaction data available"}
    
    interactions_data = [{
        'interaction_type': i.interaction_type,
        'topic': i.topic,
        'duration_minutes': i.duration_minutes,
        'score': i.score,
        'difficulty_level': i.difficulty_level,
        'engagement_score': i.engagement_score,
        'timestamp': i.timestamp
    } for i in interactions]
    
    # Get learning state for mastery
    state = await get_learning_state(student_id, db)
    topic_proficiencies = json.loads(state.topic_proficiencies) if state.topic_proficiencies else {}
    
    # Analyze mistakes
    mistake_breakdown = state_model.mistake_engine.get_mistake_breakdown(
        interactions_data,
        topic_proficiencies
    )
    
    return mistake_breakdown

