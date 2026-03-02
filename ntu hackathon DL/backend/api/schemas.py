"""
Pydantic schemas for API request/response validation
"""
from pydantic import BaseModel
from typing import Optional
from typing import Optional, List, Dict, Any
from datetime import datetime


class StudentCreate(BaseModel):
    name: str
    email: str  # Email validation can be added later if needed


class StudentResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class InteractionCreate(BaseModel):
    interaction_type: str
    topic: str
    duration_minutes: float = 0.0
    score: Optional[float] = None
    difficulty_level: str = "medium"
    engagement_score: float = 0.5
    metadata: Optional[str] = None


class InteractionResponse(BaseModel):
    id: int
    student_id: int
    interaction_type: str
    topic: str
    duration_minutes: float
    score: Optional[float]
    difficulty_level: str
    engagement_score: float
    timestamp: datetime
    
    class Config:
        from_attributes = True


class LearningStateResponse(BaseModel):
    id: int
    student_id: int
    overall_proficiency: float
    engagement_level: float
    learning_velocity: float
    consistency_score: float
    days_since_last_activity: int
    is_active: bool
    risk_level: str
    topic_proficiencies: str
    timestamp: datetime
    
    class Config:
        from_attributes = True


class RecommendationResponse(BaseModel):
    id: int
    student_id: int
    recommendation_type: str
    priority: str
    title: str
    description: str
    reasoning: str
    suggested_topic: Optional[str]
    suggested_duration: Optional[int]
    action_items: Optional[str]
    supporting_data: Optional[str]
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class DashboardData(BaseModel):
    student: StudentResponse
    learning_state: LearningStateResponse
    interactions: List[InteractionResponse]
    recommendations: List[RecommendationResponse]
    metrics: Dict[str, Any]

