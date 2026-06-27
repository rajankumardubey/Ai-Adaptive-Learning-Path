from datetime import datetime, timedelta
from typing import List, Dict
import json

class StudyPlanner:
    """Service to generate personalized study schedules"""
    
    def __init__(self):
        pass
    
    def generate_plan(self, user_id: int, difficulty_level: float, duration_days: int = 7) -> Dict:
        """Generate a week's study plan based on user's profile"""
        schedule = []
        current_date = datetime.now()
        
        for day in range(duration_days):
            date = current_date + timedelta(days=day)
            day_schedule = self._generate_daily_schedule(user_id, difficulty_level, date)
            schedule.extend(day_schedule)
        
        return {
            "schedule": schedule,
            "duration_days": duration_days,
            "estimated_hours": self._calculate_total_hours(schedule),
            "difficulty_level": difficulty_level
        }
    
    def _generate_daily_schedule(self, user_id: int, difficulty_level: float, date: datetime) -> List[Dict]:
        """Generate schedule for a specific day"""
        schedule = []
        
        # Morning session (1 hour)
        schedule.append({
            "time": "09:00 AM",
            "topic": "Core Concept Review",
            "duration": 60,
            "level": difficulty_level,
            "description": "Review and reinforce key concepts"
        })
        
        # Afternoon session (45 mins)
        schedule.append({
            "time": "02:00 PM",
            "topic": "Problem Solving",
            "duration": 45,
            "level": difficulty_level + 0.2,
            "description": "Practice problems at your level"
        })
        
        # Evening session (30 mins)
        schedule.append({
            "time": "06:00 PM",
            "topic": "Quiz Practice",
            "duration": 30,
            "level": difficulty_level,
            "description": "Test your knowledge with quizzes"
        })
        
        return schedule
    
    def _calculate_total_hours(self, schedule: List[Dict]) -> float:
        """Calculate total study hours in schedule"""
        total_minutes = sum(item.get("duration", 0) for item in schedule)
        return total_minutes / 60
    
    def adjust_schedule(self, user_id: int, feedback: str) -> Dict:
        """Adjust schedule based on user feedback"""
        # Adjust based on user feedback
        return {"message": "Schedule adjusted"}
