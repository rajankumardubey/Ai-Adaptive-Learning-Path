"""
API Route Examples for AI System Integration

Copy and modify these examples to integrate the AI system into your routes.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel

# Import the adaptive engine
from services.enhanced_adaptive_engine import EnhancedAdaptiveEngine

# Initialize router
router = APIRouter()

# Initialize engine (load trained model)
# Path can be relative to Backend directory
try:
    engine = EnhancedAdaptiveEngine('ml/training/trained_models/adaptive_model.pkl')
    print("✓ AI Model loaded successfully")
except Exception as e:
    print(f"⚠ AI Model not found: {e}. Using fallback estimation.")
    engine = EnhancedAdaptiveEngine()  # Use fallback without trained model

# ============================================================================
# Pydantic Models for Request/Response
# ============================================================================

class PerformancePredictionRequest(BaseModel):
    student_level: float  # 0-100
    course_difficulty: float  # 0-100
    engagement_score: float  # 0-1
    learning_speed: float  # 0.5-2.0
    time_spent_hours: float  # hours

class PerformancePredictionResponse(BaseModel):
    predicted_score: float
    confidence: float
    likely_completion: bool
    model_used: bool

class RecommendationResponse(BaseModel):
    course_id: int
    course_title: str
    subject: Optional[str]
    difficulty: str
    predicted_score: float
    completion_likelihood: bool
    confidence: float
    recommendation_score: float

class RecommendationsListResponse(BaseModel):
    user_id: int
    recommendations: List[RecommendationResponse]
    total_courses: int

class DifficultyAdjustmentResponse(BaseModel):
    difficulty_adjustment: float
    recommendation: str
    average_performance: float
    performance_trend: float
    suggested_action: str  # 'INCREASE', 'DECREASE', or 'MAINTAIN'

class NextLessonResponse(BaseModel):
    lesson_id: int
    lesson_title: str
    difficulty_score: float
    predicted_performance: float
    recommendation_score: float

# ============================================================================
# API Endpoints
# ============================================================================

@router.post("/predictions/performance", response_model=PerformancePredictionResponse)
async def predict_performance(request: PerformancePredictionRequest):
    """
    Predict student performance on a course
    
    Example:
    ```
    POST /api/ai/predictions/performance
    {
        "student_level": 70,
        "course_difficulty": 75,
        "engagement_score": 0.8,
        "learning_speed": 1.2,
        "time_spent_hours": 10
    }
    ```
    
    Response:
    ```
    {
        "predicted_score": 78.5,
        "confidence": 0.92,
        "likely_completion": true,
        "model_used": true
    }
    ```
    """
    try:
        prediction = engine.predict_performance(
            student_level=request.student_level,
            course_difficulty=request.course_difficulty,
            engagement_score=request.engagement_score,
            learning_speed=request.learning_speed,
            time_spent_hours=request.time_spent_hours
        )
        return PerformancePredictionResponse(**prediction)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recommendations/{user_id}")
async def get_recommendations(
    user_id: int,
    limit: int = 5,
    user_level: float = 50,
    engagement: float = 0.7,
    learning_speed: float = 1.0
) -> RecommendationsListResponse:
    """
    Get personalized course recommendations
    
    Query Parameters:
    - limit: Number of recommendations (default: 5)
    - user_level: Student's current level 0-100 (default: 50)
    - engagement: Engagement score 0-1 (default: 0.7)
    - learning_speed: Learning speed multiplier (default: 1.0)
    
    Example:
    ```
    GET /api/ai/recommendations/123?limit=5&user_level=70&engagement=0.8&learning_speed=1.2
    ```
    
    Response:
    ```
    {
        "user_id": 123,
        "recommendations": [
            {
                "course_id": 5,
                "course_title": "Advanced Python",
                "subject": "CS",
                "difficulty": "Intermediate",
                "predicted_score": 82.3,
                "completion_likelihood": true,
                "confidence": 0.88,
                "recommendation_score": 0.89
            },
            ...
        ],
        "total_courses": 3
    }
    ```
    """
    try:
        # TODO: Fetch actual courses from database
        # For now, using sample data
        available_courses = [
            {
                'id': 1,
                'title': 'Python Basics',
                'subject': 'Computer Science',
                'difficulty': 'Beginner',
                'duration_hours': 10,
                'difficulty_score': 30
            },
            {
                'id': 2,
                'title': 'Advanced Python',
                'subject': 'Computer Science',
                'difficulty': 'Intermediate',
                'duration_hours': 20,
                'difficulty_score': 60
            },
            {
                'id': 3,
                'title': 'Machine Learning Basics',
                'subject': 'Computer Science',
                'difficulty': 'Advanced',
                'duration_hours': 30,
                'difficulty_score': 80
            },
        ]
        
        recommendations = engine.get_recommendations(
            user_id=user_id,
            user_level=user_level,
            engagement=engagement,
            learning_speed=learning_speed,
            available_courses=available_courses,
            limit=limit
        )
        
        return RecommendationsListResponse(
            user_id=user_id,
            recommendations=[RecommendationResponse(**rec) for rec in recommendations],
            total_courses=len(recommendations)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recommendations/{user_id}/next-lesson")
async def get_next_lesson(
    user_id: int,
    user_level: float = 50,
    engagement: float = 0.7,
    learning_speed: float = 1.0,
    completed_lessons: Optional[List[int]] = None
) -> NextLessonResponse:
    """
    Get the recommended next lesson for a student
    
    Query Parameters:
    - user_level: Student's current level (default: 50)
    - engagement: Engagement score 0-1 (default: 0.7)
    - learning_speed: Learning speed multiplier (default: 1.0)
    - completed_lessons: List of completed lesson IDs
    
    Example:
    ```
    GET /api/ai/recommendations/123/next-lesson?user_level=70&engagement=0.8
    ```
    
    Response:
    ```
    {
        "lesson_id": 5,
        "lesson_title": "Functions and Classes",
        "difficulty_score": 65,
        "predicted_performance": 78.5,
        "recommendation_score": 0.85
    }
    ```
    """
    try:
        if completed_lessons is None:
            completed_lessons = []
        
        # TODO: Fetch actual lessons from database
        available_lessons = [
            {
                'id': 1,
                'title': 'Introduction',
                'difficulty_score': 20,
                'duration_hours': 2
            },
            {
                'id': 2,
                'title': 'Variables and Data Types',
                'difficulty_score': 30,
                'duration_hours': 3
            },
            {
                'id': 3,
                'title': 'Control Flow',
                'difficulty_score': 45,
                'duration_hours': 4
            },
            {
                'id': 4,
                'title': 'Functions',
                'difficulty_score': 60,
                'duration_hours': 5
            },
            {
                'id': 5,
                'title': 'Functions and Classes',
                'difficulty_score': 65,
                'duration_hours': 6
            },
        ]
        
        next_lesson = engine.get_next_lesson(
            user_id=user_id,
            user_level=user_level,
            engagement=engagement,
            learning_speed=learning_speed,
            completed_lessons=completed_lessons,
            available_lessons=available_lessons
        )
        
        if next_lesson is None:
            raise HTTPException(status_code=404, detail="No recommended lessons available")
        
        return NextLessonResponse(
            lesson_id=next_lesson['id'],
            lesson_title=next_lesson['title'],
            difficulty_score=next_lesson['difficulty_score'],
            predicted_performance=next_lesson['predicted_performance'],
            recommendation_score=next_lesson['recommendation_score']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/difficulty/adjust/{user_id}", response_model=DifficultyAdjustmentResponse)
async def adjust_difficulty(
    user_id: int,
    recent_performance: List[float]
):
    """
    Adjust learning difficulty based on recent performance
    
    Request Body:
    ```
    {
        "recent_performance": [65, 70, 75, 80, 85]
    }
    ```
    
    Example:
    ```
    POST /api/ai/difficulty/adjust/123
    {
        "recent_performance": [75, 78, 82, 85, 88]
    }
    ```
    
    Response:
    ```
    {
        "difficulty_adjustment": 0.15,
        "recommendation": "Increase difficulty - student is excelling",
        "average_performance": 81.6,
        "performance_trend": 3.25,
        "suggested_action": "INCREASE"
    }
    ```
    
    Action meanings:
    - INCREASE: Increase difficulty (student exceeding expectations)
    - DECREASE: Decrease difficulty (student struggling)
    - MAINTAIN: Keep current difficulty level
    """
    try:
        if not recent_performance:
            raise HTTPException(status_code=400, detail="recent_performance cannot be empty")
        
        adjustment = engine.adjust_learning_path(
            user_id=user_id,
            recent_performance=recent_performance
        )
        
        return DifficultyAdjustmentResponse(**adjustment)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Batch Operations
# ============================================================================

@router.post("/batch/predictions")
async def batch_predict_performance(
    predictions: List[PerformancePredictionRequest]
):
    """
    Predict performance for multiple students/courses at once
    
    Example:
    ```
    POST /api/ai/batch/predictions
    [
        {
            "student_level": 70,
            "course_difficulty": 75,
            "engagement_score": 0.8,
            "learning_speed": 1.2,
            "time_spent_hours": 10
        },
        {
            "student_level": 60,
            "course_difficulty": 50,
            "engagement_score": 0.7,
            "learning_speed": 0.9,
            "time_spent_hours": 8
        }
    ]
    ```
    
    Response:
    ```
    [
        {"predicted_score": 78.5, "confidence": 0.92, ...},
        {"predicted_score": 72.3, "confidence": 0.88, ...}
    ]
    ```
    """
    try:
        results = []
        for pred in predictions:
            result = engine.predict_performance(
                student_level=pred.student_level,
                course_difficulty=pred.course_difficulty,
                engagement_score=pred.engagement_score,
                learning_speed=pred.learning_speed,
                time_spent_hours=pred.time_spent_hours
            )
            results.append(result)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Model Information Endpoints
# ============================================================================

@router.get("/model/status")
async def get_model_status():
    """
    Get status of the AI model
    
    Response:
    ```
    {
        "model_loaded": true,
        "model_used": true,
        "fallback_active": false,
        "architecture": "5 -> 16 -> 1",
        "parameters": 317,
        "trained": true
    }
    ```
    """
    try:
        status = {
            "model_loaded": engine.model_loaded,
            "model_used": engine.model_loaded,
            "fallback_active": not engine.model_loaded
        }
        
        if engine.model_loaded and engine.model is not None:
            status.update(engine.model.get_model_info())
        
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/model/info")
async def get_model_info():
    """Get detailed model information"""
    try:
        if not engine.model_loaded or engine.model is None:
            return {
                "message": "Model not loaded. Using fallback estimation.",
                "status": "fallback"
            }
        
        return {
            "status": "loaded",
            "info": engine.model.get_model_info()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Notes for Implementation
# ============================================================================

"""
INTEGRATION CHECKLIST:

1. Import this router in your main app.py:
   from routes.ai_routes import router as ai_router
   app.include_router(ai_router, prefix="/api/ai", tags=["AI Services"])

2. Replace TODO sections with actual database queries:
   - get_user(user_id) - Fetch user from database
   - get_user_courses(user_id) - Get user's enrolled courses
   - get_available_courses() - Get all available courses
   - get_available_lessons() - Get all available lessons
   - get_recent_scores(user_id) - Get recent performance scores

3. Ensure the trained model exists:
   python Backend/ml/training/train.py --quick

4. Update model path if needed:
   engine = EnhancedAdaptiveEngine('path/to/model.pkl')

5. Test endpoints:
   # Prediction
   curl -X POST "http://localhost:8000/api/ai/predictions/performance" \\
     -H "Content-Type: application/json" \\
     -d '{"student_level": 70, "course_difficulty": 75, ...}'

6. Monitor performance:
   - Check predicted scores vs actual scores
   - Track recommendation acceptance rate
   - Measure performance improvement over time

BEST PRACTICES:

1. Cache user data to avoid repeated database queries
2. Update predictions periodically as user data changes
3. Monitor model accuracy and retrain with new data
4. Use batch endpoints for bulk operations
5. Implement rate limiting for production
6. Log all predictions for future analysis
7. A/B test different recommendation strategies

"""
