"""
Study ROI Optimizer
Optimizes study time allocation based on Expected Learning Gain per Minute (ELGM)
Generates time-optimized study plans (30/60/120 minutes)
"""
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
import pandas as pd
from models.bkt_model import BayesianKnowledgeTracing


class StudyROIOptimizer:
    """
    Optimizes study recommendations based on time ROI
    Prioritizes topics that offer maximum learning gain per minute
    """
    
    def __init__(self, bkt_model: BayesianKnowledgeTracing):
        self.bkt = bkt_model
    
    def calculate_elgm(
        self,
        topic: str,
        current_mastery: float,
        estimated_time_minutes: int,
        retention_risk: float = 0.0
    ) -> Dict:
        """
        Calculate Expected Learning Gain per Minute (ELGM)
        
        ELGM = (Predicted Score Improvement) / (Estimated Time Cost)
        
        Factors:
        - Current mastery gap (how much room for improvement)
        - Learning rate (how fast can student improve)
        - Retention risk (urgency factor)
        - Time efficiency (estimated attempts per minute)
        """
        # Simulate study session
        simulation = self.bkt.simulate_study_session(
            topic,
            estimated_time_minutes,
            expected_attempts=max(5, estimated_time_minutes // 3)
        )
        
        expected_gain = simulation['expected_mastery'] - current_mastery
        
        # Apply retention risk multiplier (urgent topics get higher priority)
        urgency_multiplier = 1.0 + (retention_risk * 0.5)
        adjusted_gain = expected_gain * urgency_multiplier
        
        # Calculate ELGM
        if estimated_time_minutes > 0:
            elgm = adjusted_gain / estimated_time_minutes
        else:
            elgm = 0.0
        
        # Calculate expected exam performance improvement
        # Assuming mastery translates linearly to exam score
        exam_improvement = expected_gain * 100  # Percentage points
        
        return {
            'topic': topic,
            'current_mastery': current_mastery,
            'expected_mastery': simulation['expected_mastery'],
            'expected_gain': expected_gain,
            'elgm': elgm,
            'estimated_time': estimated_time_minutes,
            'exam_improvement_pct': exam_improvement,
            'urgency_score': retention_risk,
            'confidence': simulation.get('confidence', 'medium')
        }
    
    def generate_study_plan(
        self,
        available_minutes: int,
        topic_masteries: Dict[str, float],
        retention_risks: Dict[str, float] = None,
        excluded_topics: List[str] = None
    ) -> Dict:
        """
        Generate optimized study plan for given time budget
        
        Returns:
        - Ranked list of topics with time allocation
        - Expected overall improvement
        - Time-optimized schedule
        """
        if not topic_masteries:
            return {
                'topics': [],
                'total_time': 0,
                'expected_improvement': 0.0,
                'plan': []
            }
        
        excluded = set(excluded_topics or [])
        retention_risks = retention_risks or {}
        
        # Calculate ELGM for each topic
        topic_scores = []
        
        for topic, mastery in topic_masteries.items():
            if topic in excluded:
                continue
            
            # Estimate time needed based on mastery gap
            mastery_gap = 1.0 - mastery
            if mastery_gap < 0.1:
                continue  # Skip topics already mastered
            
            # Time estimate: more time for larger gaps, but with diminishing returns
            base_time = 15  # Minimum 15 minutes
            gap_time = mastery_gap * 45  # Up to 45 more minutes for large gaps
            estimated_time = int(base_time + gap_time)
            
            retention_risk = retention_risks.get(topic, 0.0)
            
            elgm_data = self.calculate_elgm(
                topic,
                mastery,
                estimated_time,
                retention_risk
            )
            
            topic_scores.append(elgm_data)
        
        # Sort by ELGM (highest ROI first)
        topic_scores.sort(key=lambda x: x['elgm'], reverse=True)
        
        # Allocate time using greedy algorithm
        allocated_topics = []
        remaining_time = available_minutes
        total_expected_gain = 0.0
        
        for topic_data in topic_scores:
            if remaining_time <= 0:
                break
            
            time_needed = topic_data['estimated_time']
            
            # Allocate time (may be partial)
            if time_needed <= remaining_time:
                allocated_time = time_needed
                remaining_time -= allocated_time
            else:
                # Partial allocation
                allocated_time = remaining_time
                remaining_time = 0
                # Recalculate gain for partial time
                partial_simulation = self.bkt.simulate_study_session(
                    topic_data['topic'],
                    allocated_time,
                    expected_attempts=max(3, allocated_time // 3)
                )
                topic_data['expected_gain'] = partial_simulation['expected_mastery'] - topic_data['current_mastery']
                topic_data['expected_mastery'] = partial_simulation['expected_mastery']
            
            if allocated_time >= 5:  # Minimum 5 minutes to be worthwhile
                allocated_topics.append({
                    'topic': topic_data['topic'],
                    'time_minutes': allocated_time,
                    'current_mastery': topic_data['current_mastery'],
                    'expected_mastery': topic_data['expected_mastery'],
                    'expected_gain': topic_data['expected_gain'],
                    'exam_improvement_pct': topic_data['exam_improvement_pct'],
                    'elgm': topic_data['elgm'],
                    'urgency': topic_data['urgency_score']
                })
                total_expected_gain += topic_data['expected_gain']
        
        # Calculate overall expected improvement
        avg_improvement = total_expected_gain / len(allocated_topics) if allocated_topics else 0.0
        
        return {
            'topics': allocated_topics,
            'total_time': available_minutes - remaining_time,
            'expected_improvement': avg_improvement,
            'expected_exam_improvement_pct': sum(t['exam_improvement_pct'] for t in allocated_topics),
            'efficiency_score': total_expected_gain / (available_minutes - remaining_time) if (available_minutes - remaining_time) > 0 else 0.0,
            'plan': [
                {
                    'topic': t['topic'],
                    'time': t['time_minutes'],
                    'priority': 'high' if t['elgm'] > 0.01 else 'medium' if t['elgm'] > 0.005 else 'low',
                    'expected_gain': f"{t['expected_gain']:.1%}",
                    'action': f"Focus on {t['topic']} for {t['time_minutes']} minutes. Expected mastery improvement: {t['expected_gain']:.1%}"
                }
                for t in allocated_topics
            ]
        }
    
    def compare_study_strategies(
        self,
        topic: str,
        strategy_options: List[Dict]
    ) -> Dict:
        """
        Compare different study strategies for a topic
        Returns strategy comparison with ROI analysis
        """
        current_mastery = self.bkt.get_mastery(topic)
        
        comparisons = []
        
        for strategy in strategy_options:
            time_minutes = strategy.get('time_minutes', 30)
            approach = strategy.get('approach', 'practice')
            
            simulation = self.bkt.simulate_study_session(
                topic,
                time_minutes,
                expected_attempts=strategy.get('expected_attempts', time_minutes // 3)
            )
            
            expected_gain = simulation['expected_mastery'] - current_mastery
            elgm = expected_gain / time_minutes if time_minutes > 0 else 0
            
            comparisons.append({
                'approach': approach,
                'time_minutes': time_minutes,
                'expected_gain': expected_gain,
                'expected_mastery': simulation['expected_mastery'],
                'elgm': elgm,
                'recommendation': strategy.get('description', '')
            })
        
        # Sort by ELGM
        comparisons.sort(key=lambda x: x['elgm'], reverse=True)
        
        return {
            'topic': topic,
            'current_mastery': current_mastery,
            'strategies': comparisons,
            'best_strategy': comparisons[0] if comparisons else None
        }

