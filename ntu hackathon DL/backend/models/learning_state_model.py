"""
ML models for learning state prediction and evolution tracking
Enhanced with BKT, Mistake Intelligence, and Learning Twin
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json

from models.bkt_model import BayesianKnowledgeTracing
from models.mistake_intelligence import MistakeIntelligenceEngine
from models.burnout_detector import BurnoutDetector


class LearningStateModel:
    """
    Models a student's learning state and predicts future performance
    Enhanced with BKT, Mistake Intelligence, and Burnout Detection
    """
    
    def __init__(self):
        self.proficiency_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
        self.engagement_model = RandomForestRegressor(n_estimators=50, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        
        # Enhanced models
        self.bkt = BayesianKnowledgeTracing()
        self.mistake_engine = MistakeIntelligenceEngine()
        self.burnout_detector = BurnoutDetector()
    
    def extract_features(self, interactions_df: pd.DataFrame, lookback_days: int = 30) -> pd.DataFrame:
        """
        Extract features from learning interactions for state modeling
        """
        if interactions_df.empty:
            return pd.DataFrame()
        
        features = []
        
        # Time-based features
        interactions_df['timestamp'] = pd.to_datetime(interactions_df['timestamp'])
        interactions_df = interactions_df.sort_values('timestamp')
        
        # Recent activity window
        cutoff_date = interactions_df['timestamp'].max() - timedelta(days=lookback_days)
        recent_interactions = interactions_df[interactions_df['timestamp'] >= cutoff_date]
        
        if recent_interactions.empty:
            return pd.DataFrame()
        
        # Aggregate features
        feature_dict = {
            # Activity metrics
            'total_interactions': len(recent_interactions),
            'total_study_time': recent_interactions['duration_minutes'].sum(),
            'avg_session_duration': recent_interactions['duration_minutes'].mean(),
            'days_active': recent_interactions['timestamp'].dt.date.nunique(),
            
            # Performance metrics
            'avg_score': recent_interactions['score'].mean() if recent_interactions['score'].notna().any() else 0.5,
            'score_trend': self._calculate_trend(recent_interactions['score']) if recent_interactions['score'].notna().any() else 0,
            'high_score_ratio': (recent_interactions['score'] >= 0.8).sum() / len(recent_interactions) if recent_interactions['score'].notna().any() else 0,
            
            # Engagement metrics
            'avg_engagement': recent_interactions['engagement_score'].mean(),
            'engagement_trend': self._calculate_trend(recent_interactions['engagement_score']),
            
            # Topic diversity
            'unique_topics': recent_interactions['topic'].nunique(),
            'topic_concentration': self._calculate_concentration(recent_interactions['topic']),
            
            # Difficulty progression
            'avg_difficulty_score': self._difficulty_to_numeric(recent_interactions['difficulty_level']).mean(),
            'difficulty_trend': self._calculate_trend(self._difficulty_to_numeric(recent_interactions['difficulty_level'])),
            
            # Consistency
            'consistency_score': self._calculate_consistency(recent_interactions['timestamp']),
            
            # Recency
            'days_since_last_activity': (datetime.now() - recent_interactions['timestamp'].max()).days,
        }
        
        return pd.DataFrame([feature_dict])
    
    def _calculate_trend(self, series: pd.Series) -> float:
        """Calculate linear trend (slope) of a time series"""
        if len(series) < 2 or series.isna().all():
            return 0.0
        series_clean = series.dropna()
        if len(series_clean) < 2:
            return 0.0
        x = np.arange(len(series_clean))
        y = series_clean.values
        slope = np.polyfit(x, y, 1)[0]
        return float(slope)
    
    def _calculate_concentration(self, topics: pd.Series) -> float:
        """Calculate topic concentration (lower = more diverse)"""
        if topics.empty:
            return 0.0
        value_counts = topics.value_counts()
        total = len(topics)
        # Shannon entropy normalized
        proportions = value_counts / total
        entropy = -np.sum(proportions * np.log2(proportions + 1e-10))
        max_entropy = np.log2(len(value_counts) + 1e-10)
        return 1 - (entropy / max_entropy) if max_entropy > 0 else 0.0
    
    def _difficulty_to_numeric(self, difficulties: pd.Series) -> pd.Series:
        """Convert difficulty levels to numeric scores"""
        mapping = {'easy': 0.33, 'medium': 0.66, 'hard': 1.0}
        return difficulties.map(mapping).fillna(0.66)
    
    def _calculate_consistency(self, timestamps: pd.Series) -> float:
        """Calculate study consistency based on regularity of timestamps"""
        if len(timestamps) < 2:
            return 0.5
        
        timestamps = pd.to_datetime(timestamps).sort_values()
        intervals = timestamps.diff().dropna()
        
        if intervals.empty:
            return 0.5
        
        # Lower coefficient of variation = more consistent
        mean_interval = intervals.mean().total_seconds()
        std_interval = intervals.std().total_seconds()
        
        if mean_interval == 0:
            return 1.0
        
        cv = std_interval / mean_interval
        # Convert to 0-1 scale (lower CV = higher consistency)
        consistency = max(0, 1 - min(cv, 1.0))
        return float(consistency)
    
    def predict_state(self, interactions_df: pd.DataFrame) -> Dict:
        """
        Predict current learning state from interactions
        """
        features_df = self.extract_features(interactions_df)
        
        if features_df.empty:
            return self._default_state()
        
        # Calculate state metrics
        state = {
            'overall_proficiency': self._estimate_proficiency(features_df),
            'engagement_level': self._estimate_engagement(features_df),
            'learning_velocity': float(features_df['score_trend'].iloc[0]) if 'score_trend' in features_df.columns else 0.0,
            'consistency_score': float(features_df['consistency_score'].iloc[0]) if 'consistency_score' in features_df.columns else 0.5,
            'days_since_last_activity': int(features_df['days_since_last_activity'].iloc[0]) if 'days_since_last_activity' in features_df.columns else 0,
            'is_active': int(features_df['days_since_last_activity'].iloc[0]) < 7 if 'days_since_last_activity' in features_df.columns else True,
            'risk_level': self._assess_risk(features_df),
            'topic_proficiencies': self._calculate_topic_proficiencies(interactions_df)
        }
        
        return state
    
    def _estimate_proficiency(self, features_df: pd.DataFrame) -> float:
        """Estimate overall proficiency from features"""
        if features_df.empty:
            return 0.5
        
        # Weighted combination of performance indicators
        avg_score = features_df.get('avg_score', pd.Series([0.5])).iloc[0]
        score_trend = features_df.get('score_trend', pd.Series([0])).iloc[0]
        high_score_ratio = features_df.get('high_score_ratio', pd.Series([0])).iloc[0]
        difficulty_trend = features_df.get('difficulty_trend', pd.Series([0])).iloc[0]
        
        # Normalize and combine
        proficiency = (
            0.4 * avg_score +
            0.2 * max(0, min(1, 0.5 + score_trend)) +
            0.2 * high_score_ratio +
            0.2 * max(0, min(1, 0.5 + difficulty_trend * 2))
        )
        
        return float(max(0, min(1, proficiency)))
    
    def _estimate_engagement(self, features_df: pd.DataFrame) -> float:
        """Estimate engagement level from features"""
        if features_df.empty:
            return 0.5
        
        avg_engagement = features_df.get('avg_engagement', pd.Series([0.5])).iloc[0]
        engagement_trend = features_df.get('engagement_trend', pd.Series([0])).iloc[0]
        days_active = features_df.get('days_active', pd.Series([0])).iloc[0]
        consistency = features_df.get('consistency_score', pd.Series([0.5])).iloc[0]
        
        # Normalize days_active (assuming 30-day window)
        days_active_norm = min(1.0, days_active / 30.0)
        
        engagement = (
            0.3 * avg_engagement +
            0.2 * max(0, min(1, 0.5 + engagement_trend)) +
            0.3 * days_active_norm +
            0.2 * consistency
        )
        
        return float(max(0, min(1, engagement)))
    
    def _assess_risk(self, features_df: pd.DataFrame) -> str:
        """Assess risk level based on features"""
        if features_df.empty:
            return "medium"
        
        days_inactive = features_df.get('days_since_last_activity', pd.Series([0])).iloc[0]
        engagement = features_df.get('avg_engagement', pd.Series([0.5])).iloc[0]
        score_trend = features_df.get('score_trend', pd.Series([0])).iloc[0]
        
        risk_score = 0
        if days_inactive > 14:
            risk_score += 2
        elif days_inactive > 7:
            risk_score += 1
        
        if engagement < 0.3:
            risk_score += 1
        
        if score_trend < -0.1:
            risk_score += 1
        
        if risk_score >= 3:
            return "high"
        elif risk_score >= 2:
            return "medium"
        else:
            return "low"
    
    def _calculate_topic_proficiencies(self, interactions_df: pd.DataFrame) -> Dict[str, float]:
        """Calculate proficiency scores per topic"""
        if interactions_df.empty:
            return {}
        
        topic_proficiencies = {}
        
        for topic in interactions_df['topic'].unique():
            topic_data = interactions_df[interactions_df['topic'] == topic]
            
            # Average score for this topic
            scores = topic_data['score'].dropna()
            if len(scores) > 0:
                avg_score = scores.mean()
                recent_scores = scores.tail(5)
                recent_avg = recent_scores.mean() if len(recent_scores) > 0 else avg_score
                
                # Weight recent performance more
                proficiency = 0.3 * avg_score + 0.7 * recent_avg
            else:
                # Estimate from engagement and difficulty
                avg_engagement = topic_data['engagement_score'].mean()
                avg_difficulty = self._difficulty_to_numeric(topic_data['difficulty_level']).mean()
                proficiency = avg_engagement * (1 - avg_difficulty * 0.3)  # Adjust for difficulty
            
            topic_proficiencies[topic] = float(max(0, min(1, proficiency)))
        
        return topic_proficiencies
    
    def _default_state(self) -> Dict:
        """Return default state when no data available"""
        return {
            'overall_proficiency': 0.5,
            'engagement_level': 0.5,
            'learning_velocity': 0.0,
            'consistency_score': 0.5,
            'days_since_last_activity': 0,
            'is_active': True,
            'risk_level': 'medium',
            'topic_proficiencies': {}
        }

