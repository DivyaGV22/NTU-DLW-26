"""
Mistake Intelligence Engine
Classifies errors into actionable categories:
- Conceptual Gap
- Careless Error
- Speed-Based Issue
- Fragile Mastery
"""
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
import pandas as pd
from collections import defaultdict


class MistakeIntelligenceEngine:
    """
    Analyzes mistakes to identify patterns and root causes
    Provides explainable error classification
    """
    
    def __init__(self):
        self.error_patterns: Dict[str, List[Dict]] = defaultdict(list)
    
    def classify_error(
        self,
        interaction: Dict,
        topic_history: List[Dict],
        mastery_level: float
    ) -> Dict:
        """
        Classify an error into one of four categories
        Returns classification with reasoning
        """
        score = interaction.get('score', 0)
        if score >= 0.5:
            return None  # Not an error
        
        duration = interaction.get('duration_minutes', 0)
        difficulty = interaction.get('difficulty_level', 'medium')
        timestamp = interaction.get('timestamp', datetime.now())
        
        # Get recent history for this topic
        recent_errors = [
            i for i in topic_history 
            if i.get('score', 1) < 0.5 and 
            (timestamp - pd.to_datetime(i.get('timestamp', timestamp))).days <= 7
        ]
        
        error_count = len(recent_errors)
        avg_time_on_errors = np.mean([
            i.get('duration_minutes', 0) 
            for i in recent_errors if i.get('duration_minutes', 0) > 0
        ]) if recent_errors else 0
        
        # Classification logic
        classification = None
        confidence = 0.0
        reasoning = ""
        
        # 1. Conceptual Gap
        # - Repeated errors over time
        # - High time spent on errors
        # - Low mastery level
        if (error_count >= 3 and 
            avg_time_on_errors > 5 and 
            mastery_level < 0.5):
            classification = "conceptual_gap"
            confidence = min(0.9, 0.5 + (error_count / 10))
            reasoning = f"Repeated errors ({error_count} in past week) with high time investment ({avg_time_on_errors:.1f} min avg) suggest a fundamental misunderstanding of core concepts."
        
        # 2. Careless Error
        # - High mastery but sudden incorrect
        # - Low time spent
        # - Isolated error
        elif (mastery_level > 0.7 and 
              duration < 2 and 
              error_count <= 1):
            classification = "careless_error"
            confidence = 0.8
            reasoning = f"High mastery level ({mastery_level:.0%}) with very quick attempt ({duration:.1f} min) suggests a careless mistake rather than lack of understanding."
        
        # 3. Speed-Based Issue
        # - Accuracy drops when solving faster
        # - Recent correct answers but fast
        elif (duration < 3 and 
              mastery_level > 0.4 and 
              mastery_level < 0.7):
            # Check if recent correct answers took longer
            recent_correct = [
                i for i in topic_history[-5:] 
                if i.get('score', 0) >= 0.5
            ]
            if recent_correct:
                avg_correct_time = np.mean([
                    i.get('duration_minutes', 0) 
                    for i in recent_correct
                ])
                if avg_correct_time > duration * 1.5:
                    classification = "speed_issue"
                    confidence = 0.75
                    reasoning = f"Accuracy drops when solving quickly ({duration:.1f} min vs {avg_correct_time:.1f} min avg for correct). Slowing down may improve performance."
        
        # 4. Fragile Mastery
        # - Correct short-term, fails after inactivity
        # - Time gap since last attempt
        if not classification:
            if len(topic_history) > 1:
                last_attempt = topic_history[-2] if len(topic_history) > 1 else None
                if last_attempt:
                    last_score = last_attempt.get('score', 0)
                    last_time = pd.to_datetime(last_attempt.get('timestamp', timestamp))
                    days_gap = (timestamp - last_time).days
                    
                    if (last_score >= 0.5 and 
                        days_gap > 3 and 
                        mastery_level > 0.4):
                        classification = "fragile_mastery"
                        confidence = 0.7
                        reasoning = f"Previously correct ({days_gap} days ago) but failed after inactivity. Knowledge needs reinforcement through spaced repetition."
        
        # Default: Conceptual Gap if no other classification
        if not classification:
            classification = "conceptual_gap"
            confidence = 0.6
            reasoning = "Error pattern suggests need for additional concept review and practice."
        
        return {
            'classification': classification,
            'confidence': confidence,
            'reasoning': reasoning,
            'error_count': error_count,
            'mastery_level': mastery_level,
            'duration': duration
        }
    
    def detect_error_patterns(
        self,
        topic: str,
        interactions: List[Dict]
    ) -> Dict:
        """
        Detect recurring error patterns for a topic
        Returns pattern analysis
        """
        errors = [i for i in interactions if i.get('score', 1) < 0.5]
        
        if len(errors) < 2:
            return {
                'has_pattern': False,
                'pattern_type': None,
                'frequency': 0,
                'description': 'Insufficient error data for pattern detection'
            }
        
        # Analyze error frequency
        error_rate = len(errors) / len(interactions)
        
        # Check for clustering (errors close together)
        error_timestamps = [
            pd.to_datetime(i.get('timestamp', datetime.now())) 
            for i in errors
        ]
        error_timestamps.sort()
        
        clusters = []
        current_cluster = [error_timestamps[0]]
        
        for ts in error_timestamps[1:]:
            if (ts - current_cluster[-1]).days <= 2:
                current_cluster.append(ts)
            else:
                if len(current_cluster) >= 2:
                    clusters.append(current_cluster)
                current_cluster = [ts]
        
        if len(current_cluster) >= 2:
            clusters.append(current_cluster)
        
        # Pattern detection
        if error_rate > 0.5 and len(clusters) > 0:
            return {
                'has_pattern': True,
                'pattern_type': 'recurring_conceptual_errors',
                'frequency': len(clusters),
                'error_rate': error_rate,
                'description': f'Recurring errors detected: {len(clusters)} error clusters with {error_rate:.0%} error rate. Suggests persistent conceptual gaps.'
            }
        elif error_rate > 0.3:
            return {
                'has_pattern': True,
                'pattern_type': 'frequent_errors',
                'frequency': len(errors),
                'error_rate': error_rate,
                'description': f'Frequent errors ({error_rate:.0%} error rate) indicate need for focused review.'
            }
        else:
            return {
                'has_pattern': False,
                'pattern_type': None,
                'frequency': len(errors),
                'error_rate': error_rate,
                'description': 'Errors are infrequent and isolated.'
            }
    
    def get_mistake_breakdown(
        self,
        student_interactions: List[Dict],
        topic_mastery: Dict[str, float]
    ) -> Dict:
        """
        Get overall mistake breakdown across all topics
        Returns summary statistics
        """
        topic_errors = defaultdict(lambda: {'total': 0, 'classified': []})
        
        # Group by topic
        topic_interactions = defaultdict(list)
        for interaction in student_interactions:
            topic = interaction.get('topic', 'Unknown')
            topic_interactions[topic].append(interaction)
        
        # Classify errors per topic
        for topic, interactions in topic_interactions.items():
            mastery = topic_mastery.get(topic, 0.5)
            for interaction in interactions:
                if interaction.get('score', 1) < 0.5:
                    topic_errors[topic]['total'] += 1
                    classification = self.classify_error(
                        interaction,
                        interactions,
                        mastery
                    )
                    if classification:
                        topic_errors[topic]['classified'].append(classification)
        
        # Aggregate statistics
        total_errors = sum(e['total'] for e in topic_errors.values())
        classification_counts = defaultdict(int)
        
        for topic_data in topic_errors.values():
            for classification in topic_data['classified']:
                if isinstance(classification, dict):
                    classification_counts[classification.get('classification', 'unknown')] += 1
        
        if total_errors == 0:
            return {
                'total_errors': 0,
                'breakdown': {},
                'insights': ['No errors detected in recent activity.']
            }
        
        breakdown = {
            'conceptual_gap': classification_counts.get('conceptual_gap', 0),
            'careless_error': classification_counts.get('careless_error', 0),
            'speed_issue': classification_counts.get('speed_issue', 0),
            'fragile_mastery': classification_counts.get('fragile_mastery', 0)
        }
        
        # Calculate percentages
        breakdown_pct = {
            k: (v / total_errors * 100) if total_errors > 0 else 0
            for k, v in breakdown.items()
        }
        
        # Generate insights
        insights = []
        if breakdown['conceptual_gap'] > breakdown['careless_error']:
            insights.append(f"{breakdown_pct['conceptual_gap']:.0f}% of errors are conceptual gaps - focus on understanding fundamentals.")
        if breakdown['careless_error'] > total_errors * 0.3:
            insights.append(f"{breakdown_pct['careless_error']:.0f}% are careless errors - slow down and double-check work.")
        if breakdown['fragile_mastery'] > 0:
            insights.append(f"{breakdown_pct['fragile_mastery']:.0f}% indicate fragile mastery - regular review needed.")
        
        return {
            'total_errors': total_errors,
            'breakdown': breakdown,
            'breakdown_percentages': breakdown_pct,
            'insights': insights if insights else ['Error patterns are varied - continue practicing.']
        }


import numpy as np

