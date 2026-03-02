"""
Bayesian Knowledge Tracing (BKT) Model
Probabilistic mastery estimation for each topic/skill
"""
import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class BKTParameters:
    """BKT model parameters for a topic"""
    p_init: float = 0.2  # Initial probability of mastery
    p_learn: float = 0.3  # Probability of learning after each attempt
    p_slip: float = 0.1  # Probability of careless error (slip)
    p_guess: float = 0.2  # Probability of guessing correctly
    p_forget: float = 0.05  # Probability of forgetting after inactivity


class BayesianKnowledgeTracing:
    """
    Bayesian Knowledge Tracing model for mastery estimation
    Models learning as a probabilistic process
    """
    
    def __init__(self):
        self.topic_models: Dict[str, BKTParameters] = {}
        self.mastery_history: Dict[str, List[Tuple[datetime, float]]] = {}
    
    def estimate_parameters(
        self,
        topic: str,
        interactions: List[Dict]
    ) -> BKTParameters:
        """
        Estimate BKT parameters from interaction history
        Uses Expectation-Maximization approach
        """
        if not interactions:
            return BKTParameters()
        
        # Extract correctness sequence
        correct = [1 if i.get('score', 0) >= 0.5 else 0 for i in interactions]
        
        if len(correct) < 3:
            # Use default parameters for sparse data
            return BKTParameters()
        
        # Estimate p_init (initial mastery)
        first_attempts = correct[:min(5, len(correct))]
        p_init = sum(first_attempts) / len(first_attempts)
        
        # Estimate p_learn (learning rate)
        # Look at improvement over time
        if len(correct) >= 5:
            first_half = correct[:len(correct)//2]
            second_half = correct[len(correct)//2:]
            improvement = np.mean(second_half) - np.mean(first_half)
            p_learn = max(0.1, min(0.5, improvement * 0.5))
        else:
            p_learn = 0.3
        
        # Estimate p_slip (careless error rate)
        # High mastery but incorrect = slip
        high_mastery_errors = 0
        high_mastery_total = 0
        running_mastery = p_init
        
        for i, c in enumerate(correct):
            if running_mastery > 0.7 and c == 0:
                high_mastery_errors += 1
            if running_mastery > 0.7:
                high_mastery_total += 1
            # Update running mastery estimate
            if c == 1:
                running_mastery = running_mastery + (1 - running_mastery) * p_learn
            else:
                running_mastery = running_mastery * (1 - p_learn)
        
        p_slip = high_mastery_errors / max(high_mastery_total, 1)
        p_slip = max(0.05, min(0.3, p_slip))
        
        # Estimate p_guess (guessing rate)
        # Low mastery but correct = guess
        low_mastery_correct = 0
        low_mastery_total = 0
        running_mastery = p_init
        
        for i, c in enumerate(correct):
            if running_mastery < 0.3 and c == 1:
                low_mastery_correct += 1
            if running_mastery < 0.3:
                low_mastery_total += 1
            if c == 1:
                running_mastery = running_mastery + (1 - running_mastery) * p_learn
            else:
                running_mastery = running_mastery * (1 - p_learn)
        
        p_guess = low_mastery_correct / max(low_mastery_total, 1)
        p_guess = max(0.1, min(0.4, p_guess))
        
        return BKTParameters(
            p_init=max(0.1, min(0.9, p_init)),
            p_learn=max(0.1, min(0.5, p_learn)),
            p_slip=max(0.05, min(0.3, p_slip)),
            p_guess=max(0.1, min(0.4, p_guess)),
            p_forget=0.05
        )
    
    def update_mastery(
        self,
        topic: str,
        is_correct: bool,
        timestamp: datetime,
        interactions: List[Dict] = None
    ) -> float:
        """
        Update mastery probability after an interaction
        Returns new mastery probability
        """
        # Get or estimate parameters
        if topic not in self.topic_models:
            if interactions:
                self.topic_models[topic] = self.estimate_parameters(topic, interactions)
            else:
                self.topic_models[topic] = BKTParameters()
        
        params = self.topic_models[topic]
        
        # Get current mastery
        if topic in self.mastery_history and self.mastery_history[topic]:
            current_mastery = self.mastery_history[topic][-1][1]
            
            # Apply forgetting if there's a time gap
            if len(self.mastery_history[topic]) > 1:
                last_time = self.mastery_history[topic][-1][0]
                days_gap = (timestamp - last_time).days
                if days_gap > 0:
                    # Exponential decay for forgetting
                    current_mastery = current_mastery * (1 - params.p_forget) ** min(days_gap, 7)
        else:
            current_mastery = params.p_init
        
        # Update based on observation
        if is_correct:
            # P(mastery | correct) = P(correct | mastery) * P(mastery) / P(correct)
            p_correct_given_mastery = 1 - params.p_slip
            p_correct_given_not_mastery = params.p_guess
            p_correct = (p_correct_given_mastery * current_mastery + 
                        p_correct_given_not_mastery * (1 - current_mastery))
            
            if p_correct > 0:
                new_mastery = (p_correct_given_mastery * current_mastery) / p_correct
            else:
                new_mastery = current_mastery
            
            # Apply learning
            new_mastery = new_mastery + (1 - new_mastery) * params.p_learn
        else:
            # P(mastery | incorrect) = P(incorrect | mastery) * P(mastery) / P(incorrect)
            p_incorrect_given_mastery = params.p_slip
            p_incorrect_given_not_mastery = 1 - params.p_guess
            p_incorrect = (p_incorrect_given_mastery * current_mastery + 
                          p_incorrect_given_not_mastery * (1 - current_mastery))
            
            if p_incorrect > 0:
                new_mastery = (p_incorrect_given_mastery * current_mastery) / p_incorrect
            else:
                new_mastery = current_mastery
        
        # Clamp to [0, 1]
        new_mastery = max(0.0, min(1.0, new_mastery))
        
        # Store history
        if topic not in self.mastery_history:
            self.mastery_history[topic] = []
        self.mastery_history[topic].append((timestamp, new_mastery))
        
        return new_mastery
    
    def get_mastery(self, topic: str) -> float:
        """Get current mastery probability for a topic"""
        if topic in self.mastery_history and self.mastery_history[topic]:
            return self.mastery_history[topic][-1][1]
        elif topic in self.topic_models:
            return self.topic_models[topic].p_init
        else:
            return 0.2  # Default initial mastery
    
    def predict_retention(
        self,
        topic: str,
        days_ahead: int
    ) -> float:
        """
        Predict mastery after N days of inactivity
        Models forgetting curve
        """
        current_mastery = self.get_mastery(topic)
        
        if topic not in self.topic_models:
            return current_mastery
        
        params = self.topic_models[topic]
        # Exponential decay
        predicted = current_mastery * (1 - params.p_forget) ** min(days_ahead, 30)
        return max(0.0, min(1.0, predicted))
    
    def simulate_study_session(
        self,
        topic: str,
        minutes: int,
        expected_attempts: int = 10
    ) -> Dict:
        """
        Simulate a study session and predict mastery improvement
        Returns expected mastery gain
        """
        current_mastery = self.get_mastery(topic)
        
        if topic not in self.topic_models:
            return {
                'current_mastery': current_mastery,
                'expected_mastery': current_mastery,
                'expected_gain': 0.0,
                'confidence': 'low'
            }
        
        params = self.topic_models[topic]
        
        # Simulate expected improvement
        # Each correct attempt increases mastery
        simulated_mastery = current_mastery
        attempts_per_minute = expected_attempts / minutes if minutes > 0 else 1
        
        for _ in range(int(expected_attempts)):
            # Probability of correct answer
            p_correct = (simulated_mastery * (1 - params.p_slip) + 
                        (1 - simulated_mastery) * params.p_guess)
            
            # Expected mastery update
            if p_correct > 0.5:  # More likely correct
                simulated_mastery = simulated_mastery + (1 - simulated_mastery) * params.p_learn
        
        expected_gain = simulated_mastery - current_mastery
        
        return {
            'current_mastery': current_mastery,
            'expected_mastery': min(1.0, simulated_mastery),
            'expected_gain': expected_gain,
            'confidence': 'high' if len(self.mastery_history.get(topic, [])) > 5 else 'medium'
        }

