from fastapi import APIRouter, Depends, UploadFile, File, Form
from models.user import User
from auth.dependencies import get_current_user
from services.ai_solver import AIDoubSolver
from services.study_planner import StudyPlanner
from services.adaptive_engine import AdaptiveEngine
from ml.recommendation_model import RecommendationModel
from database.crud import get_all_courses

router = APIRouter()

@router.post("/solve-doubt")
async def solve_doubt(
    question: str = Form(...),
    image: UploadFile = File(None),
    current_user: User = Depends(get_current_user)
):
    """Solve student's doubt using AI"""
    solver = AIDoubSolver()
    
    image_text = None
    if image:
        image_text = await solver.extract_text_from_image(image)
    
    answer = solver.solve(question, image_text)
    return answer

@router.get("/study-plan")
async def get_study_plan(current_user: User = Depends(get_current_user)):
    """Generate personalized study plan"""
    planner = StudyPlanner()
    plan = planner.generate_plan(current_user.id, current_user.learning_level)
    return plan

@router.get("/recommendations")
async def get_recommendations(current_user: User = Depends(get_current_user)):
    """Get personalized course recommendations"""
    engine = AdaptiveEngine()
    recommendations = engine.get_recommendations(current_user.id)
    return recommendations

@router.post("/adaptive-difficulty")
async def adjust_difficulty(difficulty_score: float, current_user: User = Depends(get_current_user)):
    """Adjust learning difficulty based on performance"""
    engine = AdaptiveEngine()
    updated_difficulty = engine.adjust_difficulty(current_user.id, difficulty_score)
    return {"new_difficulty": updated_difficulty}


# Public endpoints (no auth) for demo/demo integration
@router.post("/solve-doubt-public")
async def solve_doubt_public(question: str = Form(...), image: UploadFile = File(None)):
    """Solve student's doubt without requiring authentication (demo only)"""
    solver = AIDoubSolver()
    image_text = None
    if image:
        image_text = await solver.extract_text_from_image(image)
    answer = solver.solve(question, image_text)
    return answer


@router.get("/recommendations-public")
async def recommendations_public(q: str):
    """Return simple content recommendations based on query using trained ML model (demo)"""
    try:
        model = RecommendationModel()
        # Try to load courses from DB; fallback to a small sample
        courses = get_all_courses() or [
            {"id": 1, "title": "Calculus 101", "description": "Limits, derivatives, integrals and applications."},
            {"id": 2, "title": "Physics Basics", "description": "Newtonian mechanics, forces, motion and energy."},
            {"id": 3, "title": "English Grammar", "description": "Tenses, sentence structure, and writing skills."},
            {"id": 4, "title": "Linear Algebra", "description": "Vectors, matrices, eigenvalues and applications."},
        ]
        recs = model.recommend_content(user_profile=q, content_list=courses, top_k=5)
        return {"query": q, "recommendations": recs}
    except Exception as e:
        return {"error": str(e), "recommendations": []}
