from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProgressBase(BaseModel):
    completion_percentage: float
    score: float

class ProgressCreate(ProgressBase):
    user_id: int
    chapter_id: int

class Progress(ProgressBase):
    id: int
    user_id: int
    chapter_id: int
    is_completed: bool
    started_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ProgressStats(BaseModel):
    total_hours: float
    lessons_completed: int
    average_score: float
    current_streak: int
    courses_in_progress: int
