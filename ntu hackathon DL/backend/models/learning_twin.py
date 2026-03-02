"""
Digital Learning Twin
Simulates student's knowledge state over time
Predicts retention, "what-if" scenarios, and future performance
"""
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
from models.bkt_model import BayesianKnowledgeTracing


class DigitalLearningTwin:
    """
    Digital twin that simulates learning state evolution
    Supports predictive scenarios and retention modeling
    """
    
    def __init__(self, bkt_model: BayesianKnowledgeTracing):
        self.bkt = bkt_model
        self.scenarios: List[Dict] = []
    
    def predict_retention_decay(
        self,
        topic: str,
        days_ahead: int = 7
    ) -> Dict:
        """
        Predict how mastery will decay without practice
        Returns retention curve over time
        """
        current_mastery = self.bkt.get_mastery(topic)
        
        if topic not in self.bkt.topic_models:
            return {
                'topic': topic,
                'current_mastery': current_mastery,
                'predicted_mastery': current_mastery,
                'decay_rate': 0.0,
                'days_to_threshold': None,
                'retention_curve': []
            }
        
        params = self.bkt.topic_models[topic]
        retention_curve = []
        
        for day in range(0, days_ahead + 1, 1):
            predicted = current_mastery * (1 - params.p_forget) ** min(day, 30)
            retention_curve.append({
                'day': day,
                'mastery': max(0.0, min(1.0, predicted)),
                'decay': current_mastery - predicted
            })
        
        final_mastery = retention_curve[-1]['mastery']
        decay_rate = (current_mastery - final_mastery) / days_ahead if days_ahead > 0 else 0
        
        # Find when mastery drops below threshold (e.g., 0.6)
        threshold = 0.6
        days_to_threshold = None
        for point in retention_curve:
            if point['mastery'] < threshold:
                days_to_threshold = point['day']
                break
        
        return {
            'topic': topic,
            'current_mastery': current_mastery,
            'predicted_mastery': final_mastery,
            'decay_rate': decay_rate,
            'days_to_threshold': days_to_threshold,
            'retention_curve': retention_curve,
            'warning': f"If you don't revise {topic} in {days_to_threshold} days, mastery will likely drop to {final_mastery:.0%}." if days_to_threshold else None
        }
    
    def simulate_study_scenario(
        self,
        topic: str,
        study_minutes: int,
        days_from_now: int = 0
    ) -> Dict:
        """
        Simulate "what if I study X minutes" scenario
        Returns predicted mastery improvement and exam impact
        """
        current_mastery = self.bkt.get_mastery(topic)
        
        # Apply retention decay if studying in the future
        if days_from_now > 0:
            retention_prediction = self.predict_retention_decay(topic, days_from_now)
            starting_mastery = retention_prediction['predicted_mastery']
        else:
            starting_mastery = current_mastery
        
        # Simulate study session
        simulation = self.bkt.simulate_study_session(
            topic,
            study_minutes,
            expected_attempts=max(5, study_minutes // 3)
        )
        
        expected_mastery = simulation['expected_mastery']
        mastery_gain = expected_mastery - starting_mastery
        
        # Estimate exam performance impact
        # Assuming mastery translates to exam score
        current_exam_score = starting_mastery * 100
        expected_exam_score = expected_mastery * 100
        exam_improvement = expected_exam_score - current_exam_score
        
        return {
            'topic': topic,
            'scenario': f"Study {study_minutes} minutes",
            'current_mastery': starting_mastery,
            'expected_mastery': expected_mastery,
            'mastery_gain': mastery_gain,
            'current_exam_score': current_exam_score,
            'expected_exam_score': expected_exam_score,
            'exam_improvement_pct': exam_improvement,
            'time_investment': study_minutes,
            'roi': mastery_gain / study_minutes if study_minutes > 0 else 0,
            'recommendation': f"If you practice {topic} for {study_minutes} minutes, expected exam performance increases by {exam_improvement:.1f}%."
        }
    
    def simulate_inactivity_scenario(
        self,
        topic: str,
        days_inactive: int
    ) -> Dict:
        """
        Simulate "what if I don't study for X days" scenario
        """
        current_mastery = self.bkt.get_mastery(topic)
        retention = self.predict_retention_decay(topic, days_inactive)
        
        predicted_mastery = retention['predicted_mastery']
        mastery_loss = current_mastery - predicted_mastery
        
        return {
            'topic': topic,
            'scenario': f"No study for {days_inactive} days",
            'current_mastery': current_mastery,
            'predicted_mastery': predicted_mastery,
            'mastery_loss': mastery_loss,
            'current_exam_score': current_mastery * 100,
            'predicted_exam_score': predicted_mastery * 100,
            'exam_decline_pct': mastery_loss * 100,
            'days_inactive': days_inactive,
            'warning': f"If you don't revise {topic} in {days_inactive} days, your mastery will likely drop to {predicted_mastery:.0%}."
        }
    
    def compare_scenarios(
        self,
        topic: str,
        scenarios: List[Dict]
    ) -> Dict:
        """
        Compare multiple "what-if" scenarios for a topic
        """
        results = []
        
        for scenario in scenarios:
            scenario_type = scenario.get('type', 'study')
            
            if scenario_type == 'study':
                result = self.simulate_study_scenario(
                    topic,
                    scenario.get('minutes', 30),
                    scenario.get('days_from_now', 0)
                )
            elif scenario_type == 'inactivity':
                result = self.simulate_inactivity_scenario(
                    topic,
                    scenario.get('days', 7)
                )
            else:
                continue
            
            results.append(result)
        
        # Sort by impact
        if results:
            results.sort(
                key=lambda x: x.get('exam_improvement_pct', 0) or -x.get('exam_decline_pct', 0),
                reverse=True
            )
        
        return {
            'topic': topic,
            'current_mastery': self.bkt.get_mastery(topic),
            'scenarios': results,
            'best_scenario': results[0] if results else None,
            'worst_scenario': results[-1] if results and len(results) > 1 else None
        }
    
    def predict_exam_performance(
        self,
        topics: List[str],
        exam_date: datetime,
        study_plan: Dict[str, int] = None
    ) -> Dict:
        """
        Predict overall exam performance based on current state and study plan
        """
        current_date = datetime.now()
        days_until_exam = (exam_date - current_date).days
        
        topic_predictions = []
        total_mastery = 0.0
        
        for topic in topics:
            current_mastery = self.bkt.get_mastery(topic)
            
            # Apply study plan if provided
            if study_plan and topic in study_plan:
                study_minutes = study_plan[topic]
                study_simulation = self.simulate_study_scenario(topic, study_minutes)
                mastery_after_study = study_simulation['expected_mastery']
            else:
                mastery_after_study = current_mastery
            
            # Apply retention decay until exam
            if days_until_exam > 0:
                retention = self.predict_retention_decay(topic, days_until_exam)
                # Start from mastery after study
                predicted_mastery = mastery_after_study * (1 - 0.05) ** min(days_until_exam, 30)
            else:
                predicted_mastery = mastery_after_study
            
            topic_predictions.append({
                'topic': topic,
                'current_mastery': current_mastery,
                'predicted_mastery': predicted_mastery,
                'exam_score': predicted_mastery * 100
            })
            
            total_mastery += predicted_mastery
        
        avg_mastery = total_mastery / len(topics) if topics else 0.0
        predicted_exam_score = avg_mastery * 100
        
        return {
            'exam_date': exam_date.isoformat(),
            'days_until_exam': days_until_exam,
            'predicted_exam_score': predicted_exam_score,
            'average_mastery': avg_mastery,
            'topic_predictions': topic_predictions,
            'confidence': 'high' if days_until_exam <= 30 else 'medium',
            'recommendation': f"Based on current progress, predicted exam score: {predicted_exam_score:.0f}%. Focus on topics below 70% mastery."
        }

