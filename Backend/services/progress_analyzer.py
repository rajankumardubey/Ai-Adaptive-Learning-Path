from typing import Dict, List
import numpy as np
from database.crud import get_user_progress, get_user_assessments

class ProgressAnalyzer:
    """Service for analyzing student progress and performance"""
    
    @staticmethod
    def get_student_stats(user_id: int) -> Dict:
        """Get comprehensive student statistics"""
        progress = get_user_progress(user_id)
        assessments = get_user_assessments(user_id)
        
        return {
            "total_hours": ProgressAnalyzer._calculate_total_hours(progress),
            "lessons_completed": len([p for p in progress if p.get("is_completed")]),
            "average_score": ProgressAnalyzer._calculate_average_score(assessments),
            "current_streak": ProgressAnalyzer._calculate_streak(progress),
            "courses_in_progress": len(set(p.get("course_id") for p in progress))
        }
    
    @staticmethod
    def get_user_progress(user_id: int) -> List[Dict]:
        """Get user's detailed progress"""
        progress = get_user_progress(user_id)
        return progress
    
    @staticmethod
    def get_learning_velocity(user_id: int) -> float:
        """Calculate how fast user is learning (lessons per day)"""
        progress = get_user_progress(user_id)
        if not progress:
            return 0.0
        
        # Calculate lessons per day
        total_lessons = len(progress)
        days_active = ProgressAnalyzer._calculate_days_active(progress)
        
        if days_active == 0:
            return 0.0
        
        return total_lessons / days_active
    
    @staticmethod
    def get_problem_areas(user_id: int) -> List[str]:
        """Identify areas where user struggles"""
        assessments = get_user_assessments(user_id)
        
        low_score_topics = []
        for assessment in assessments:
            if assessment.get("score", 100) < 60:
                low_score_topics.append(assessment.get("topic"))
        
        return list(set(low_score_topics))
    
    @staticmethod
    def _calculate_total_hours(progress: List[Dict]) -> float:
        """Calculate total study hours"""
        total_minutes = sum(p.get("duration_minutes", 0) for p in progress)
        return total_minutes / 60
    
    @staticmethod
    def _calculate_average_score(assessments: List[Dict]) -> float:
        """Calculate average assessment score"""
        if not assessments:
            return 0.0
        scores = [a.get("score", 0) for a in assessments]
        return np.mean(scores)
    
    @staticmethod
    def _calculate_streak(progress: List[Dict]) -> int:
        """Calculate current learning streak (days)"""
        # Implementation depends on data structure
        return 0  # Placeholder
    
    @staticmethod
    def _calculate_days_active(progress: List[Dict]) -> int:
        """Calculate number of days user has been active"""
        return max(1, len(set(p.get("date") for p in progress)))
