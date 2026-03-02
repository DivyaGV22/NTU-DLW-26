"""
Inactivity & Burnout Risk Detector
Detects signs of cognitive overload, fatigue, and learning stagnation
"""
from typing import Dict, List
from datetime import datetime, timedelta
import pandas as pd
import numpy as np


class BurnoutDetector:
    """
    Detects burnout, fatigue, and inactivity risks
    Provides early warning signals for intervention
    """
    
    def __init__(self):
        self.risk_thresholds = {
            'high': 0.7,
            'medium': 0.4,
            'low': 0.2
        }
    
    def detect_burnout_signals(
        self,
        recent_interactions: List[Dict],
        learning_state: Dict
    ) -> Dict:
        """
        Detect burnout and fatigue signals from recent activity
        """
        if not recent_interactions:
            return {
                'risk_level': 'low',
                'signals': [],
                'recommendation': 'No recent activity data available.'
            }
        
        signals = []
        risk_score = 0.0
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame(recent_interactions)
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
        
        # Signal 1: Sudden drop in accuracy
        if len(df) >= 5:
            recent_scores = df['score'].tail(5) if 'score' in df.columns else pd.Series()
            earlier_scores = df['score'].head(len(df) - 5) if 'score' in df.columns else pd.Series()
            
            if len(recent_scores) > 0 and len(earlier_scores) > 0:
                recent_avg = recent_scores.mean()
                earlier_avg = earlier_scores.mean()
                accuracy_drop = earlier_avg - recent_avg
                
                if accuracy_drop > 0.2:
                    signals.append({
                        'type': 'accuracy_drop',
                        'severity': 'high' if accuracy_drop > 0.3 else 'medium',
                        'description': f'Accuracy dropped by {accuracy_drop:.0%} recently. Possible fatigue or cognitive overload.',
                        'evidence': f'Recent average: {recent_avg:.0%}, Previous: {earlier_avg:.0%}'
                    })
                    risk_score += 0.3 if accuracy_drop > 0.3 else 0.2
        
        # Signal 2: Reduced session time
        if 'duration_minutes' in df.columns:
            recent_duration = df['duration_minutes'].tail(5).mean() if len(df) >= 5 else df['duration_minutes'].mean()
            earlier_duration = df['duration_minutes'].head(len(df) - 5).mean() if len(df) >= 5 else df['duration_minutes'].mean()
            
            if earlier_duration > 0:
                duration_reduction = (earlier_duration - recent_duration) / earlier_duration
                
                if duration_reduction > 0.3:
                    signals.append({
                        'type': 'reduced_engagement',
                        'severity': 'high' if duration_reduction > 0.5 else 'medium',
                        'description': f'Session time reduced by {duration_reduction:.0%}. May indicate fatigue or loss of motivation.',
                        'evidence': f'Recent avg: {recent_duration:.1f} min, Previous: {earlier_duration:.1f} min'
                    })
                    risk_score += 0.25 if duration_reduction > 0.5 else 0.15
        
        # Signal 3: Increased careless mistakes
        if 'score' in df.columns and 'duration_minutes' in df.columns:
            recent_errors = df[df['score'] < 0.5].tail(10)
            if len(recent_errors) >= 3:
                quick_errors = recent_errors[recent_errors['duration_minutes'] < 2]
                if len(quick_errors) / len(recent_errors) > 0.5:
                    signals.append({
                        'type': 'careless_increase',
                        'severity': 'medium',
                        'description': f'{len(quick_errors)}/{len(recent_errors)} recent errors were quick attempts. May indicate rushing due to fatigue.',
                        'evidence': 'High proportion of errors with <2 min duration'
                    })
                    risk_score += 0.2
        
        # Signal 4: Inactivity period
        days_since_activity = learning_state.get('days_since_last_activity', 0)
        if days_since_activity > 7:
            signals.append({
                'type': 'inactivity',
                'severity': 'high' if days_since_activity > 14 else 'medium',
                'description': f'No activity for {days_since_activity} days. Risk of knowledge decay and loss of momentum.',
                'evidence': f'Last activity: {days_since_activity} days ago'
            })
            risk_score += 0.3 if days_since_activity > 14 else 0.2
        
        # Signal 5: Low engagement level
        engagement = learning_state.get('engagement_level', 0.5)
        if engagement < 0.3:
            signals.append({
                'type': 'low_engagement',
                'severity': 'medium',
                'description': f'Engagement level is {engagement:.0%}. May indicate burnout or lack of motivation.',
                'evidence': f'Current engagement: {engagement:.0%}'
            })
            risk_score += 0.15
        
        # Signal 6: Declining learning velocity
        velocity = learning_state.get('learning_velocity', 0.0)
        if velocity < -0.1:
            signals.append({
                'type': 'negative_velocity',
                'severity': 'high' if velocity < -0.2 else 'medium',
                'description': f'Learning velocity is negative ({velocity:.1%}). Performance is declining over time.',
                'evidence': f'Learning velocity: {velocity:.1%}'
            })
            risk_score += 0.25 if velocity < -0.2 else 0.15
        
        # Determine overall risk level
        if risk_score >= self.risk_thresholds['high']:
            risk_level = 'high'
            recommendation = 'High risk of burnout or cognitive overload detected. Consider taking a break and reviewing study strategies.'
        elif risk_score >= self.risk_thresholds['medium']:
            risk_level = 'medium'
            recommendation = 'Some signs of fatigue detected. Monitor your study patterns and ensure adequate rest.'
        else:
            risk_level = 'low'
            recommendation = 'No significant burnout signals detected. Continue with current study patterns.'
        
        return {
            'risk_level': risk_level,
            'risk_score': risk_score,
            'signals': signals,
            'signal_count': len(signals),
            'recommendation': recommendation,
            'intervention_suggested': risk_level in ['high', 'medium']
        }
    
    def detect_stagnation(
        self,
        interactions: List[Dict],
        lookback_days: int = 14
    ) -> Dict:
        """
        Detect learning stagnation (no improvement over time)
        """
        if len(interactions) < 5:
            return {
                'is_stagnant': False,
                'description': 'Insufficient data for stagnation analysis.'
            }
        
        df = pd.DataFrame(interactions)
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            cutoff = datetime.now() - timedelta(days=lookback_days)
            df = df[df['timestamp'] >= cutoff]
        
        if 'score' not in df.columns or len(df) < 5:
            return {
                'is_stagnant': False,
                'description': 'Insufficient score data for analysis.'
            }
        
        scores = df['score'].dropna()
        if len(scores) < 5:
            return {
                'is_stagnant': False,
                'description': 'Insufficient score data.'
            }
        
        # Calculate trend
        x = np.arange(len(scores))
        slope = np.polyfit(x, scores.values, 1)[0]
        
        # Stagnation criteria: slope close to zero and low variance
        variance = scores.var()
        is_stagnant = abs(slope) < 0.01 and variance < 0.05
        
        return {
            'is_stagnant': is_stagnant,
            'trend_slope': float(slope),
            'score_variance': float(variance),
            'average_score': float(scores.mean()),
            'description': 'Performance appears stagnant with minimal improvement.' if is_stagnant else 'Performance shows variation or improvement.',
            'recommendation': 'Try different study strategies or seek help if stagnation persists.' if is_stagnant else None
        }

