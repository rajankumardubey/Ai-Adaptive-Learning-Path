from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ChapterBase(BaseModel):
    title: str
    content: str
    order: int

class ChapterCreate(ChapterBase):
    course_id: int

class Chapter(ChapterBase):
    id: int
    course_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class CourseBase(BaseModel):
    title: str
    description: str
    difficulty_level: float = 1.0

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int
    created_at: datetime
    updated_at: datetime
    chapters: List[Chapter] = []

    class Config:
        from_attributes = True
