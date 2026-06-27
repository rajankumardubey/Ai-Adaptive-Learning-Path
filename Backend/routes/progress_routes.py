from fastapi import APIRouter, Depends
from typing import List
from models.user import User
from models.progress import Progress, ProgressStats
from auth.dependencies import get_current_user
from services.progress_analyzer import ProgressAnalyzer

router = APIRouter()

@router.get("/user/{user_id}")
async def get_user_progress(user_id: int, current_user: User = Depends(get_current_user)):
    """Get user's progress across all courses"""
    progress = ProgressAnalyzer.get_user_progress(user_id)
    return progress

@router.get("/")
async def get_my_progress(current_user: User = Depends(get_current_user)):
    """Get current user's progress"""
    return ProgressAnalyzer.get_user_progress(current_user.id)

@router.post("/update")
async def update_progress(progress_data: dict, current_user: User = Depends(get_current_user)):
    """Update user's progress"""
    return {"message": "Progress updated"}

@router.get("/stats")
async def get_stats(current_user: User = Depends(get_current_user)):
    """Get user's statistics"""
    stats = ProgressAnalyzer.get_student_stats(current_user.id)
    return stats
