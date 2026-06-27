from pydantic import BaseModel
from typing import List, Optional

class QuestionBase(BaseModel):
    question: str
    options: List[str]
    correct_answer: int
    explanation: Optional[str] = None

class QuestionCreate(QuestionBase):
    chapter_id: int

class Question(QuestionBase):
    id: int
    chapter_id: int

    class Config:
        from_attributes = True

class QuizResponse(BaseModel):
    questions: List[Question]
    title: str
    total_questions: int
