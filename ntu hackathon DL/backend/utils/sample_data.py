"""
Script to generate sample learning interaction data for testing
"""
import sys
import os
from datetime import datetime, timedelta
import random

# Add backend directory to path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

from database.models import get_db, Student, LearningInteraction
from sqlalchemy.orm import Session


def generate_sample_data(db: Session, student_id: int, num_interactions: int = 30):
    """Generate sample learning interactions for a student"""
    
    topics = ['Mathematics', 'Physics', 'Chemistry', 'Biology', 'Computer Science', 'English']
    interaction_types = ['study', 'quiz', 'assignment', 'video', 'reading']
    difficulty_levels = ['easy', 'medium', 'hard']
    
    # Generate interactions over the past 30 days
    base_date = datetime.now() - timedelta(days=30)
    
    interactions = []
    for i in range(num_interactions):
        # Random date within the past 30 days
        days_ago = random.randint(0, 30)
        timestamp = base_date + timedelta(days=days_ago, hours=random.randint(9, 21))
        
        interaction_type = random.choice(interaction_types)
        topic = random.choice(topics)
        
        # Generate realistic scores (improving over time)
        days_since_start = (timestamp - base_date).days
        base_score = 0.4 + (days_since_start / 30) * 0.3  # Improve from 0.4 to 0.7
        score = max(0.3, min(1.0, base_score + random.uniform(-0.15, 0.15)))
        
        # Only quizzes and assignments have scores
        if interaction_type not in ['quiz', 'assignment']:
            score = None
        
        # Duration based on interaction type
        duration_map = {
            'study': (30, 120),
            'quiz': (15, 45),
            'assignment': (60, 180),
            'video': (10, 60),
            'reading': (20, 90)
        }
        duration = random.randint(*duration_map[interaction_type])
        
        # Engagement score (correlated with performance)
        engagement = max(0.3, min(1.0, score + random.uniform(-0.2, 0.2))) if score else random.uniform(0.4, 0.9)
        
        # Difficulty (harder topics have lower scores)
        difficulty = random.choice(difficulty_levels)
        if difficulty == 'hard' and score:
            score = max(0.2, score - 0.1)
        elif difficulty == 'easy' and score:
            score = min(1.0, score + 0.1)
        
        interaction = LearningInteraction(
            student_id=student_id,
            interaction_type=interaction_type,
            topic=topic,
            duration_minutes=duration,
            score=score,
            difficulty_level=difficulty,
            engagement_score=engagement,
            timestamp=timestamp
        )
        
        interactions.append(interaction)
    
    db.add_all(interactions)
    db.commit()
    
    print(f"Generated {num_interactions} sample interactions for student {student_id}")
    return interactions


if __name__ == "__main__":
    from database.models import create_engine, Base, sessionmaker
    import os
    
    # Create database session
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(backend_dir, "learning_analytics.db")
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    # Create a sample student if none exists
    student = db.query(Student).first()
    if not student:
        student = Student(
            name="Sample Student",
            email="student@example.com"
        )
        db.add(student)
        db.commit()
        db.refresh(student)
        print(f"Created sample student: {student.name} (ID: {student.id})")
    
    # Generate sample data
    generate_sample_data(db, student.id, num_interactions=50)
    db.close()
    print("Sample data generation complete!")

