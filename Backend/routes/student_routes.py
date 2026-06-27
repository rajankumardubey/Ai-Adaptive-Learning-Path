from fastapi import APIRouter, Depends
from models.user import User
from models.progress import ProgressStats
from auth.dependencies import get_current_user
from services.progress_analyzer import ProgressAnalyzer

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard(current_user: User = Depends(get_current_user)):
    """Get student dashboard data"""
    stats = ProgressAnalyzer.get_student_stats(current_user.id)
    return {
        "user": current_user,
        "stats": stats
    }

@router.get("/profile")
async def get_profile(current_user: User = Depends(get_current_user)):
    """Get student profile"""
    return current_user

@router.put("/profile")
async def update_profile(updates: dict, current_user: User = Depends(get_current_user)):
    """Update student profile"""
    # Update logic here
    return {"message": "Profile updated"}
