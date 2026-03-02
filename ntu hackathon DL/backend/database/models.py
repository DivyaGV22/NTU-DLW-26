"""
Database models for learning interactions and student state
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import json

Base = declarative_base()

class Student(Base):
    """Student profile and metadata"""
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    interactions = relationship("LearningInteraction", back_populates="student")
    states = relationship("LearningState", back_populates="student")
    recommendations = relationship("Recommendation", back_populates="student")


class LearningInteraction(Base):
    """Individual learning events and activities"""
    __tablename__ = "learning_interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    
    # Interaction details
    interaction_type = Column(String, nullable=False)  # 'study', 'quiz', 'assignment', 'video', 'reading'
    topic = Column(String, nullable=False)
    duration_minutes = Column(Float, default=0.0)
    score = Column(Float, nullable=True)  # For quizzes/assignments
    difficulty_level = Column(String, default="medium")  # 'easy', 'medium', 'hard'
    engagement_score = Column(Float, default=0.5)  # 0-1 scale
    
    # Metadata
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    extra_data = Column(Text, nullable=True)  # JSON string for additional data (renamed from metadata to avoid SQLAlchemy conflict)
    
    # Relationships
    student = relationship("Student", back_populates="interactions")


class LearningState(Base):
    """Snapshot of student's learning state at a point in time"""
    __tablename__ = "learning_states"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    
    # State metrics
    overall_proficiency = Column(Float, default=0.5)  # 0-1 scale
    engagement_level = Column(Float, default=0.5)  # 0-1 scale
    learning_velocity = Column(Float, default=0.0)  # Rate of improvement
    consistency_score = Column(Float, default=0.5)  # Regularity of study
    
    # Topic-specific proficiency (stored as JSON)
    topic_proficiencies = Column(Text, nullable=True)  # JSON: {"topic": score}
    
    # Behavioral indicators
    days_since_last_activity = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    risk_level = Column(String, default="low")  # 'low', 'medium', 'high'
    
    # Timestamp
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    student = relationship("Student", back_populates="states")


class Recommendation(Base):
    """AI-generated recommendations for students"""
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    
    # Recommendation details
    recommendation_type = Column(String, nullable=False)  # 'study', 'review', 'practice', 'break'
    priority = Column(String, default="medium")  # 'low', 'medium', 'high', 'urgent'
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    
    # Explainability
    reasoning = Column(Text, nullable=False)  # Why this recommendation
    supporting_data = Column(Text, nullable=True)  # JSON with evidence
    
    # Action details
    suggested_topic = Column(String, nullable=True)
    suggested_duration = Column(Integer, nullable=True)  # minutes
    action_items = Column(Text, nullable=True)  # JSON array of steps
    
    # Status
    status = Column(String, default="pending")  # 'pending', 'viewed', 'completed', 'dismissed'
    created_at = Column(DateTime, default=datetime.utcnow)
    viewed_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    student = relationship("Student", back_populates="recommendations")


def get_db():
    """Database session factory"""
    engine = create_engine("sqlite:///./learning_analytics.db", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

