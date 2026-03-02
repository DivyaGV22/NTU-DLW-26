"""
AI-powered recommendation engine for personalized learning guidance
Enhanced with ROI optimization, Learning Twin, and Mistake Intelligence
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import pandas as pd
import json

from models.study_roi_optimizer import StudyROIOptimizer
from models.learning_twin import DigitalLearningTwin
from models.mistake_intelligence import MistakeIntelligenceEngine


class RecommendationEngine:
    """
    Generates personalized, explainable recommendations based on learning state
    Enhanced with ROI optimization and Learning Twin integration
    """
    
    def __init__(self, bkt_model=None):
        # Initialize enhanced models if BKT provided
        if bkt_model:
            self.roi_optimizer = StudyROIOptimizer(bkt_model)
            self.learning_twin = DigitalLearningTwin(bkt_model)
        else:
            self.roi_optimizer = None
            self.learning_twin = None
        
        self.mistake_engine = MistakeIntelligenceEngine()
        self.recommendation_templates = {
            'study': {
                'low_activity': {
                    'title': 'Resume Your Learning Journey',
                    'description': 'You haven\'t been active recently. Starting with a short session can help you get back on track.',
                    'reasoning_template': 'You\'ve been inactive for {days} days. Regular study helps maintain knowledge retention.'
                },
                'low_proficiency': {
                    'title': 'Focus on Core Concepts',
                    'description': 'Your proficiency in {topic} could benefit from focused review and practice.',
                    'reasoning_template': 'Your current proficiency in {topic} is {proficiency:.0%}. Reviewing fundamentals will strengthen your understanding.'
                },
                'declining_scores': {
                    'title': 'Review Recent Material',
                    'description': 'Your recent performance shows a decline. Reviewing previous topics can help identify gaps.',
                    'reasoning_template': 'Your scores have decreased by {trend:.0%} recently. Reviewing foundational concepts can help address this.'
                }
            },
            'practice': {
                'weak_topic': {
                    'title': 'Practice {topic}',
                    'description': 'Extra practice in {topic} will help improve your proficiency from {current:.0%} to your target level.',
                    'reasoning_template': 'Your proficiency in {topic} is {current:.0%}, which is below your overall average. Focused practice can help close this gap.'
                },
                'inconsistent_performance': {
                    'title': 'Build Consistency',
                    'description': 'Your performance varies significantly. Regular practice sessions will help stabilize your results.',
                    'reasoning_template': 'Your score variance is {variance:.0%}, indicating inconsistent understanding. Regular practice can help.'
                }
            },
            'review': {
                'forgetting_curve': {
                    'title': 'Review {topic}',
                    'description': 'It\'s been {days} days since you last studied {topic}. A quick review will reinforce your memory.',
                    'reasoning_template': 'Research shows that reviewing material after {days} days significantly improves retention.'
                },
                'high_difficulty': {
                    'title': 'Revisit Challenging Topics',
                    'description': 'You struggled with {topic} previously. A review with different examples might help.',
                    'reasoning_template': 'Your average score on {topic} was {score:.0%}, indicating this topic needs reinforcement.'
                }
            },
            'break': {
                'overwork': {
                    'title': 'Take a Short Break',
                    'description': 'You\'ve been studying intensively. A break can help prevent burnout and improve retention.',
                    'reasoning_template': 'You\'ve studied for {hours} hours in the past {days} days. Rest is important for effective learning.'
                },
                'low_engagement': {
                    'title': 'Recharge and Refocus',
                    'description': 'Your engagement has been low. A break might help you return with renewed focus.',
                    'reasoning_template': 'Your engagement level is {engagement:.0%}. Taking time to recharge can improve your learning effectiveness.'
                }
            },
            'accelerate': {
                'high_performance': {
                    'title': 'Challenge Yourself',
                    'description': 'You\'re performing excellently! Try more advanced topics or increase difficulty.',
                    'reasoning_template': 'Your proficiency is {proficiency:.0%} and scores are trending upward. You\'re ready for more challenging material.'
                },
                'fast_learner': {
                    'title': 'Explore Advanced Topics',
                    'description': 'Your learning velocity is high. Consider exploring more advanced concepts in {topic}.',
                    'reasoning_template': 'Your learning velocity is {velocity:.2f}, indicating rapid progress. Advanced topics can maximize your growth.'
                }
            }
        }
    
    def generate_recommendations(
        self,
        learning_state: Dict,
        recent_interactions: pd.DataFrame,
        historical_interactions: pd.DataFrame
    ) -> List[Dict]:
        """
        Generate personalized recommendations based on learning state
        """
        recommendations = []
        
        # --- Safe extraction of proficiency/mastery signals ---
        # Fix: earlier code referenced these variables before assignment, causing 500 errors.
        topic_proficiencies = learning_state.get('topic_proficiencies') or {}
        if not isinstance(topic_proficiencies, dict):
            topic_proficiencies = {}

        topic_masteries = learning_state.get('bkt_mastery') or topic_proficiencies
        if not isinstance(topic_masteries, dict):
            topic_masteries = topic_proficiencies

        # Check for burnout risk
        burnout_risk = learning_state.get('burnout_risk', 'low')
        if burnout_risk in ['high', 'medium']:
            rec = self._create_burnout_recommendation(learning_state)
            if rec:
                recommendations.append(rec)
        
        # Check for inactivity with Learning Twin prediction
        days_inactive = learning_state.get('days_since_last_activity', 0)
        if days_inactive > 3:
            rec = self._create_inactivity_recommendation(learning_state)
            if rec:
                recommendations.append(rec)
            
            # Add retention risk warnings from Learning Twin
            if self.learning_twin and topic_masteries:
                for topic, mastery in list(topic_masteries.items())[:3]:
                    retention = self.learning_twin.predict_retention_decay(topic, days_inactive + 7)
                    if retention.get('days_to_threshold') and retention['days_to_threshold'] <= days_inactive + 7:
                        rec = self._create_retention_risk_recommendation(topic, retention, learning_state)
                        if rec:
                            recommendations.append(rec)
        
        # ROI-optimized study plans
        if self.roi_optimizer and topic_masteries:
            for time_budget in [30, 60, 120]:
                study_plan = self.roi_optimizer.generate_study_plan(
                    time_budget,
                    topic_masteries,
                    retention_risks={}  # Can be enhanced with retention data
                )
                if study_plan['topics']:
                    rec = self._create_roi_study_plan_recommendation(time_budget, study_plan, learning_state)
                    if rec:
                        recommendations.append(rec)
                        break  # Only add one time-optimized plan
        
        # Check for low proficiency topics with BKT mastery
        if topic_masteries:
            weak_topics = self._identify_weak_topics(topic_masteries, learning_state.get('overall_proficiency', 0.5))
            for topic in weak_topics[:2]:  # Top 2 weak topics
                rec = self._create_topic_practice_recommendation(topic, topic_masteries[topic], learning_state)
                if rec:
                    recommendations.append(rec)
                
                # Add mistake intelligence insights
                if not recent_interactions.empty:
                    topic_interactions = recent_interactions[recent_interactions['topic'] == topic].to_dict('records')
                    if topic_interactions:
                        mistake_breakdown = self.mistake_engine.get_mistake_breakdown(
                            topic_interactions,
                            {topic: topic_masteries[topic]}
                        )
                        if mistake_breakdown.get('total_errors', 0) > 0:
                            rec = self._create_mistake_intelligence_recommendation(topic, mistake_breakdown, learning_state)
                            if rec:
                                recommendations.append(rec)
        
        # Check for declining performance
        if not recent_interactions.empty and len(recent_interactions) >= 3:
            score_trend = self._calculate_score_trend(recent_interactions)
            if score_trend < -0.1:
                rec = self._create_review_recommendation(score_trend, recent_interactions)
                if rec:
                    recommendations.append(rec)
        
        # Check for topics needing review (forgetting curve)
        review_recs = self._create_forgetting_curve_recommendations(historical_interactions, topic_proficiencies)
        recommendations.extend(review_recs[:2])  # Top 2 review recommendations
        
        # Check for accelerated learning opportunities
        if learning_state.get('learning_velocity', 0) > 0.1 and learning_state.get('overall_proficiency', 0) > 0.7:
            rec = self._create_acceleration_recommendation(learning_state, topic_proficiencies)
            if rec:
                recommendations.append(rec)
        
        # Check for overwork / need for break
        if not recent_interactions.empty:
            study_hours = recent_interactions['duration_minutes'].sum() / 60
            days_span = (recent_interactions['timestamp'].max() - recent_interactions['timestamp'].min()).days + 1
            if study_hours > 20 and days_span <= 7 and learning_state.get('engagement_level', 0.5) < 0.4:
                rec = self._create_break_recommendation(study_hours, days_span, learning_state)
                if rec:
                    recommendations.append(rec)
        
        # Sort by priority and return top 5
        recommendations = sorted(recommendations, key=lambda x: self._priority_to_score(x['priority']), reverse=True)
        return recommendations[:5]
    
    def _create_inactivity_recommendation(self, state: Dict) -> Optional[Dict]:
        """Create recommendation for inactive students"""
        days = state.get('days_since_last_activity', 0)
        if days < 3:
            return None
        
        template = self.recommendation_templates['study']['low_activity']
        
        priority = 'urgent' if days > 14 else 'high' if days > 7 else 'medium'
        
        return {
            'recommendation_type': 'study',
            'priority': priority,
            'title': template['title'],
            'description': template['description'],
            'reasoning': template['reasoning_template'].format(days=days),
            'suggested_topic': None,
            'suggested_duration': 15 if days < 7 else 30,
            'action_items': json.dumps([
                'Start with a 15-minute review session',
                'Choose a familiar topic to rebuild momentum',
                'Set a daily study reminder'
            ]),
            'supporting_data': json.dumps({
                'days_inactive': days,
                'risk_level': state.get('risk_level', 'medium')
            })
        }
    
    def _identify_weak_topics(self, topic_proficiencies: Dict[str, float], overall_proficiency: float) -> List[str]:
        """Identify topics with below-average proficiency"""
        weak_topics = [
            topic for topic, prof in topic_proficiencies.items()
            if prof < overall_proficiency * 0.8
        ]
        return sorted(weak_topics, key=lambda t: topic_proficiencies[t])
    
    def _create_topic_practice_recommendation(self, topic: str, proficiency: float, state: Dict) -> Optional[Dict]:
        """Create recommendation for practicing weak topics"""
        template = self.recommendation_templates['practice']['weak_topic']
        
        priority = 'high' if proficiency < 0.4 else 'medium'
        
        return {
            'recommendation_type': 'practice',
            'priority': priority,
            'title': template['title'].format(topic=topic),
            'description': template['description'].format(
                topic=topic,
                current=proficiency,
                target=state.get('overall_proficiency', 0.7)
            ),
            'reasoning': template['reasoning_template'].format(
                topic=topic,
                current=proficiency
            ),
            'suggested_topic': topic,
            'suggested_duration': 30,
            'action_items': json.dumps([
                f'Review key concepts in {topic}',
                'Complete practice exercises',
                'Take a short quiz to assess understanding'
            ]),
            'supporting_data': json.dumps({
                'topic': topic,
                'current_proficiency': proficiency,
                'overall_proficiency': state.get('overall_proficiency', 0.5)
            })
        }
    
    def _calculate_score_trend(self, interactions: pd.DataFrame) -> float:
        """Calculate trend in scores over time"""
        scores = interactions['score'].dropna()
        if len(scores) < 3:
            return 0.0
        
        # Split into halves and compare
        mid = len(scores) // 2
        recent_avg = scores.iloc[mid:].mean()
        earlier_avg = scores.iloc[:mid].mean()
        
        return (recent_avg - earlier_avg) / max(earlier_avg, 0.1)
    
    def _create_review_recommendation(self, trend: float, interactions: pd.DataFrame) -> Optional[Dict]:
        """Create recommendation for declining performance"""
        template = self.recommendation_templates['study']['declining_scores']
        
        # Find most common topic in recent interactions
        recent_topics = interactions['topic'].value_counts()
        main_topic = recent_topics.index[0] if len(recent_topics) > 0 else None
        
        return {
            'recommendation_type': 'review',
            'priority': 'high',
            'title': template['title'],
            'description': template['description'],
            'reasoning': template['reasoning_template'].format(trend=abs(trend)),
            'suggested_topic': main_topic,
            'suggested_duration': 45,
            'action_items': json.dumps([
                'Review previous study materials',
                'Identify specific areas of confusion',
                'Practice with easier problems first'
            ]),
            'supporting_data': json.dumps({
                'score_trend': float(trend),
                'recent_avg_score': float(interactions['score'].tail(5).mean())
            })
        }
    
    def _create_forgetting_curve_recommendations(
        self,
        interactions: pd.DataFrame,
        topic_proficiencies: Dict[str, float]
    ) -> List[Dict]:
        """Create recommendations based on forgetting curve (spaced repetition)"""
        if interactions.empty:
            return []
        
        recommendations = []
        now = datetime.now()
        
        # Group by topic and find last interaction
        for topic in interactions['topic'].unique():
            topic_interactions = interactions[interactions['topic'] == topic]
            last_interaction = topic_interactions['timestamp'].max()
            days_since = (now - pd.to_datetime(last_interaction)).days
            
            # Recommend review if > 7 days and proficiency exists
            if days_since > 7 and topic in topic_proficiencies:
                template = self.recommendation_templates['review']['forgetting_curve']
                
                rec = {
                    'recommendation_type': 'review',
                    'priority': 'medium' if days_since < 14 else 'high',
                    'title': template['title'].format(topic=topic),
                    'description': template['description'].format(days=days_since, topic=topic),
                    'reasoning': template['reasoning_template'].format(days=days_since),
                    'suggested_topic': topic,
                    'suggested_duration': 20,
                    'action_items': json.dumps([
                        f'Quick review of {topic} concepts',
                        'Test yourself with key questions',
                        'Note any forgotten details'
                    ]),
                    'supporting_data': json.dumps({
                        'topic': topic,
                        'days_since_last_study': days_since,
                        'proficiency': topic_proficiencies[topic]
                    })
                }
                recommendations.append(rec)
        
        return sorted(recommendations, key=lambda x: x['supporting_data'], reverse=True)
    
    def _create_acceleration_recommendation(self, state: Dict, topic_proficiencies: Dict[str, float]) -> Optional[Dict]:
        """Create recommendation for accelerated learners"""
        template = self.recommendation_templates['accelerate']['high_performance']
        
        # Find strongest topic
        if topic_proficiencies:
            strongest_topic = max(topic_proficiencies.items(), key=lambda x: x[1])[0]
        else:
            strongest_topic = None
        
        return {
            'recommendation_type': 'accelerate',
            'priority': 'medium',
            'title': template['title'],
            'description': template['description'],
            'reasoning': template['reasoning_template'].format(
                proficiency=state.get('overall_proficiency', 0.7),
                velocity=state.get('learning_velocity', 0.1)
            ),
            'suggested_topic': strongest_topic,
            'suggested_duration': 60,
            'action_items': json.dumps([
                'Explore advanced concepts',
                'Try challenging problems',
                'Consider teaching others (peer learning)'
            ]),
            'supporting_data': json.dumps({
                'proficiency': state.get('overall_proficiency', 0.7),
                'learning_velocity': state.get('learning_velocity', 0.1),
                'engagement': state.get('engagement_level', 0.5)
            })
        }
    
    def _create_break_recommendation(self, study_hours: float, days: int, state: Dict) -> Optional[Dict]:
        """Create recommendation for taking a break"""
        template = self.recommendation_templates['break']['overwork']
        
        return {
            'recommendation_type': 'break',
            'priority': 'medium',
            'title': template['title'],
            'description': template['description'],
            'reasoning': template['reasoning_template'].format(
                hours=study_hours,
                days=days
            ),
            'suggested_topic': None,
            'suggested_duration': 0,
            'action_items': json.dumps([
                'Take a 1-2 hour break',
                'Engage in a different activity',
                'Return refreshed for better learning'
            ]),
            'supporting_data': json.dumps({
                'study_hours': study_hours,
                'days_span': days,
                'engagement_level': state.get('engagement_level', 0.5)
            })
        }
    
    def _priority_to_score(self, priority: str) -> int:
        """Convert priority to numeric score for sorting"""
        mapping = {'urgent': 4, 'high': 3, 'medium': 2, 'low': 1}
        return mapping.get(priority, 2)
    
    def _create_burnout_recommendation(self, state: Dict) -> Optional[Dict]:
        """Create recommendation for burnout risk"""
        burnout_risk = state.get('burnout_risk', 'low')
        signals = state.get('burnout_signals', [])
        
        if burnout_risk == 'low':
            return None
        
        signal_descriptions = [s.get('description', '') for s in signals[:3]]
        
        return {
            'recommendation_type': 'break',
            'priority': 'high' if burnout_risk == 'high' else 'medium',
            'title': 'Take a Break - Burnout Risk Detected',
            'description': f'Signs of {burnout_risk} burnout risk detected. Rest is important for effective learning.',
            'reasoning': '; '.join(signal_descriptions) if signal_descriptions else 'Multiple signals indicate potential fatigue or cognitive overload.',
            'suggested_topic': None,
            'suggested_duration': 0,
            'action_items': json.dumps([
                'Take a 1-2 hour break',
                'Engage in a different activity',
                'Review study schedule and reduce intensity if needed',
                'Return refreshed for better learning'
            ]),
            'supporting_data': json.dumps({
                'risk_level': burnout_risk,
                'signal_count': len(signals),
                'signals': [s.get('type') for s in signals]
            })
        }
    
    def _create_retention_risk_recommendation(self, topic: str, retention: Dict, state: Dict) -> Optional[Dict]:
        """Create recommendation based on Learning Twin retention prediction"""
        days_to_threshold = retention.get('days_to_threshold')
        if not days_to_threshold:
            return None
        
        return {
            'recommendation_type': 'review',
            'priority': 'high' if days_to_threshold <= 3 else 'medium',
            'title': f'Urgent: Review {topic} to Prevent Knowledge Decay',
            'description': retention.get('warning', f'Your mastery in {topic} is at risk of dropping below threshold.'),
            'reasoning': f'Learning Twin predicts mastery will drop to {retention.get("predicted_mastery", 0):.0%} if not reviewed within {days_to_threshold} days.',
            'suggested_topic': topic,
            'suggested_duration': 20,
            'action_items': json.dumps([
                f'Review {topic} concepts within {days_to_threshold} days',
                'Focus on key fundamentals',
                'Take a quick practice quiz to reinforce memory'
            ]),
            'supporting_data': json.dumps({
                'topic': topic,
                'current_mastery': retention.get('current_mastery', 0),
                'predicted_mastery': retention.get('predicted_mastery', 0),
                'days_to_threshold': days_to_threshold
            })
        }
    
    def _create_roi_study_plan_recommendation(self, time_budget: int, study_plan: Dict, state: Dict) -> Optional[Dict]:
        """Create recommendation for ROI-optimized study plan"""
        if not study_plan.get('topics'):
            return None
        
        topics = study_plan['topics']
        top_topic = topics[0] if topics else None
        
        return {
            'recommendation_type': 'study',
            'priority': 'high',
            'title': f'Optimized {time_budget}-Minute Study Plan',
            'description': f'AI-optimized study plan for {time_budget} minutes. Expected improvement: {study_plan.get("expected_improvement", 0):.1%}',
            'reasoning': f'ROI analysis identified {len(topics)} topics with highest learning gain per minute. Expected exam improvement: {study_plan.get("expected_exam_improvement_pct", 0):.1f}%.',
            'suggested_topic': top_topic.get('topic') if top_topic else None,
            'suggested_duration': time_budget,
            'action_items': json.dumps([item.get('action', '') for item in study_plan.get('plan', [])[:5]]),
            'supporting_data': json.dumps({
                'time_budget': time_budget,
                'expected_improvement': study_plan.get('expected_improvement', 0),
                'efficiency_score': study_plan.get('efficiency_score', 0),
                'topics_count': len(topics)
            })
        }
    
    def _create_mistake_intelligence_recommendation(self, topic: str, mistake_breakdown: Dict, state: Dict) -> Optional[Dict]:
        """Create recommendation based on mistake intelligence analysis"""
        total_errors = mistake_breakdown.get('total_errors', 0)
        if total_errors == 0:
            return None
        
        breakdown = mistake_breakdown.get('breakdown', {})
        insights = mistake_breakdown.get('insights', [])
        
        # Determine primary error type
        primary_error = max(breakdown.items(), key=lambda x: x[1]) if breakdown else None
        
        if primary_error:
            error_type, count = primary_error
            error_pct = (count / total_errors * 100) if total_errors > 0 else 0
            
            error_descriptions = {
                'conceptual_gap': 'Conceptual gaps detected',
                'careless_error': 'Careless errors detected',
                'speed_issue': 'Speed-related issues detected',
                'fragile_mastery': 'Fragile mastery detected'
            }
            
            return {
                'recommendation_type': 'practice',
                'priority': 'high' if error_type == 'conceptual_gap' else 'medium',
                'title': f'Mistake Analysis: {topic}',
                'description': f'{error_descriptions.get(error_type, "Error patterns")} in {topic}. {error_pct:.0f}% of errors are {error_type.replace("_", " ")}.',
                'reasoning': '; '.join(insights) if insights else f'Analysis of {total_errors} errors reveals specific patterns requiring targeted practice.',
                'suggested_topic': topic,
                'suggested_duration': 30,
                'action_items': json.dumps([
                    f'Review {topic} with focus on {error_type.replace("_", " ")}',
                    'Practice similar problems',
                    'Identify root cause of repeated errors'
                ]),
                'supporting_data': json.dumps({
                    'topic': topic,
                    'total_errors': total_errors,
                    'error_breakdown': breakdown,
                    'primary_error_type': error_type
                })
            }
        
        return None

