"""
Enhanced Adaptive Engine with ML Model Integration
"""
import numpy as np
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import json
import sys

# Try to import the trained model
try:
    sys.path.insert(0, str(Path(__file__).parent.parent / "training"))
    from adaptive_model import AdaptiveLearningModel
except ImportError:
    AdaptiveLearningModel = None


class EnhancedAdaptiveEngine:
    """
    Enhanced adaptive learning recommendation engine with ML model support
    Provides intelligent recommendations based on student performance prediction
    """
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize the adaptive engine
        
        Args:
            model_path: Path to trained model file (optional)
        """
        self.model = None
        self.model_loaded = False
        
        if model_path and Path(model_path).exists():
            self.load_model(model_path)
    
    def load_model(self, model_path: str) -> bool:
        """
        Load a trained model
        
        Args:
            model_path: Path to model file
            
        Returns:
            True if model loaded successfully
        """
        try:
            if AdaptiveLearningModel is None:
                print("Warning: AdaptiveLearningModel not available")
                return False
            
            self.model = AdaptiveLearningModel()
            self.model.load_model(model_path)
            self.model_loaded = True
            print(f"Model loaded successfully from {model_path}")
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model_loaded = False
            return False
    
    def predict_performance(self, 
                           student_level: float,
                           course_difficulty: float,
                           engagement_score: float,
                           learning_speed: float,
                           time_spent_hours: float) -> Dict:
        """
        Predict student performance for a course
        
        Args:
            student_level: Student's current learning level (0-100)
            course_difficulty: Course difficulty score (0-100)
            engagement_score: Student's engagement level (0-1)
            learning_speed: Student's learning speed multiplier (0.5-2.0)
            time_spent_hours: Time spent on course
            
        Returns:
            Dictionary with prediction and confidence
        """
        if not self.model_loaded or self.model is None:
            return self._estimate_performance(
                student_level, course_difficulty, engagement_score, 
                learning_speed, time_spent_hours
            )
        
        try:
            features = np.array([[
                student_level,
                course_difficulty,
                engagement_score,
                learning_speed,
                time_spent_hours
            ]])
            
            prediction = self.model.predict(features)[0]
            
            # Calculate confidence based on how well-aligned features are
            difficulty_alignment = 1 - abs(student_level - course_difficulty) / 100
            confidence = (difficulty_alignment * 0.5 + engagement_score * 0.5)
            
            return {
                'predicted_score': float(prediction),
                'confidence': float(np.clip(confidence, 0, 1)),
                'likely_completion': prediction > 50,
                'model_used': True
            }
        except Exception as e:
            print(f"Error in prediction: {e}")
            return self._estimate_performance(
                student_level, course_difficulty, engagement_score,
                learning_speed, time_spent_hours
            )
    
    def _estimate_performance(self, 
                             student_level: float,
                             course_difficulty: float,
                             engagement_score: float,
                             learning_speed: float,
                             time_spent_hours: float) -> Dict:
        """Fallback performance estimation (non-ML based)"""
        # Simple heuristic-based estimation
        difficulty_penalty = abs(student_level - course_difficulty) / 100
        estimated_score = (
            student_level * 0.3 +
            (100 - difficulty_penalty * 100) * 0.4 +
            engagement_score * 100 * 0.3
        )
        estimated_score = np.clip(estimated_score, 0, 100)
        
        return {
            'predicted_score': float(estimated_score),
            'confidence': float(0.5),  # Lower confidence for non-ML
            'likely_completion': estimated_score > 50,
            'model_used': False
        }
    
    def get_recommendations(self, 
                           user_id: int,
                           user_level: float,
                           engagement: float,
                           learning_speed: float,
                           available_courses: List[Dict],
                           limit: int = 5) -> List[Dict]:
        """
        Get personalized course recommendations
        
        Args:
            user_id: Student ID
            user_level: Student's current level
            engagement: Student's engagement score
            learning_speed: Student's learning speed
            available_courses: List of available courses with difficulty info
            limit: Number of recommendations to return
            
        Returns:
            Ranked list of course recommendations
        """
        recommendations = []
        
        for course in available_courses:
            # Assume time spent to be average course hours
            estimated_time = course.get('duration_hours', 10)
            
            prediction = self.predict_performance(
                user_level,
                course.get('difficulty_score', 50),
                engagement,
                learning_speed,
                estimated_time
            )
            
            recommendation = {
                'course_id': course['id'],
                'course_title': course['title'],
                'subject': course.get('subject'),
                'difficulty': course.get('difficulty'),
                'predicted_score': prediction['predicted_score'],
                'completion_likelihood': prediction['likely_completion'],
                'confidence': prediction['confidence'],
                'recommendation_score': self._calculate_recommendation_score(
                    user_level, 
                    course.get('difficulty_score', 50),
                    prediction['predicted_score'],
                    prediction['confidence']
                )
            }
            recommendations.append(recommendation)
        
        # Sort by recommendation score
        recommendations.sort(key=lambda x: x['recommendation_score'], reverse=True)
        
        return recommendations[:limit]
    
    def _calculate_recommendation_score(self,
                                       student_level: float,
                                       course_difficulty: float,
                                       predicted_score: float,
                                       confidence: float) -> float:
        """
        Calculate overall recommendation score
        Factors: predicted performance, alignment with level, confidence
        """
        # Prefer courses where student will perform well
        performance_score = predicted_score / 100
        
        # Prefer appropriately difficult courses (not too easy, not too hard)
        difficulty_alignment = 1 - abs(student_level - course_difficulty) / 100
        
        # Composite score
        score = (
            performance_score * 0.4 +
            difficulty_alignment * 0.4 +
            confidence * 0.2
        )
        
        return float(score)
    
    def adjust_learning_path(self,
                            user_id: int,
                            recent_performance: List[float]) -> Dict:
        """
        Adjust learning difficulty based on recent performance
        
        Args:
            user_id: Student ID
            recent_performance: List of recent performance scores
            
        Returns:
            Adjustment recommendations
        """
        if not recent_performance:
            return {'adjustment': 0, 'recommendation': 'Continue current path'}
        
        avg_performance = np.mean(recent_performance)
        performance_trend = np.polyfit(range(len(recent_performance)), recent_performance, 1)[0]
        
        adjustment = 0
        recommendation = ""
        
        if avg_performance > 80:
            adjustment = 0.15  # Increase difficulty by 15%
            recommendation = "Increase difficulty - student is excelling"
        elif avg_performance < 50:
            adjustment = -0.20  # Decrease difficulty by 20%
            recommendation = "Decrease difficulty - student is struggling"
        elif performance_trend > 5:
            adjustment = 0.10  # Student is improving
            recommendation = "Slight increase - student is improving"
        elif performance_trend < -5:
            adjustment = -0.10  # Student is declining
            recommendation = "Slight decrease - performance declining"
        else:
            recommendation = "Maintain current difficulty level"
        
        return {
            'difficulty_adjustment': float(adjustment),
            'recommendation': recommendation,
            'average_performance': float(avg_performance),
            'performance_trend': float(performance_trend),
            'suggested_action': 'INCREASE' if adjustment > 0 else 'DECREASE' if adjustment < 0 else 'MAINTAIN'
        }
    
    def get_next_lesson(self,
                       user_id: int,
                       user_level: float,
                       engagement: float,
                       learning_speed: float,
                       completed_lessons: List[int],
                       available_lessons: List[Dict]) -> Optional[Dict]:
        """
        Recommend the next lesson for the student
        
        Args:
            user_id: Student ID
            user_level: Current learning level
            engagement: Engagement score
            learning_speed: Learning speed
            completed_lessons: IDs of completed lessons
            available_lessons: List of available lessons
            
        Returns:
            Recommended next lesson
        """
        # Filter uncompleted lessons
        uncompleted = [l for l in available_lessons if l['id'] not in completed_lessons]
        
        if not uncompleted:
            return None
        
        # Score each lesson
        scored_lessons = []
        for lesson in uncompleted:
            prediction = self.predict_performance(
                user_level,
                lesson.get('difficulty_score', 50),
                engagement,
                learning_speed,
                lesson.get('duration_hours', 5)
            )
            
            # Prefer lessons where student will have good (but not too easy) performance
            is_good_difficulty = 50 < prediction['predicted_score'] < 85
            difficulty_bonus = 0.5 if is_good_difficulty else 0
            
            score = prediction['predicted_score'] * 0.5 + difficulty_bonus * 50
            
            scored_lessons.append({
                **lesson,
                'recommendation_score': score,
                'predicted_performance': prediction['predicted_score']
            })
        
        # Return top-scored lesson
        return max(scored_lessons, key=lambda x: x['recommendation_score'])
