from fastapi import APIRouter, Depends
from typing import List
from models.course import Course, CourseCreate, Chapter
from models.user import User
from auth.dependencies import get_current_user
from database.crud import get_all_courses, get_course_by_id

router = APIRouter()

@router.get("/", response_model=List[Course])
async def list_courses(current_user: User = Depends(get_current_user)):
    """Get all available courses"""
    return get_all_courses()

@router.post("/", response_model=Course)
async def create_course(course: CourseCreate, current_user: User = Depends(get_current_user)):
    """Create a new course (admin only)"""
    # Add admin check here
    return {"id": 1, **course.dict()}

@router.get("/{course_id}", response_model=Course)
async def get_course(course_id: int, current_user: User = Depends(get_current_user)):
    """Get course by ID"""
    course = get_course_by_id(course_id)
    return course

@router.get("/{course_id}/chapters")
async def get_chapters(course_id: int, current_user: User = Depends(get_current_user)):
    """Get all chapters in a course"""
    return {"chapters": []}

@router.get("/{course_id}/chapters/{chapter_id}")
async def get_chapter(course_id: int, chapter_id: int, current_user: User = Depends(get_current_user)):
    """Get specific chapter"""
    return {"id": chapter_id, "title": "Chapter Title", "content": "Content"}
