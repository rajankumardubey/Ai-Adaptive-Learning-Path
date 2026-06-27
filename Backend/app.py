from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from config import settings
from routes import auth_routes, student_routes, course_routes, progress_routes, ai_routes
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Adaptive Learning Platform API",
    description="AI-powered adaptive learning path system",
    version="0.1.0",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_routes.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(student_routes.router, prefix="/api/student", tags=["Student"])
app.include_router(course_routes.router, prefix="/api/courses", tags=["Courses"])
app.include_router(progress_routes.router, prefix="/api/progress", tags=["Progress"])
app.include_router(ai_routes.router, prefix="/api/ai", tags=["AI Services"])

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to Adaptive Learning Platform API"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "0.1.0"}

# Error handlers
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"An error occurred: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
