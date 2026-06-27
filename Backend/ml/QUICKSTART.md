# Backend AI Training - Quick Start

## What Was Created

A complete **Machine Learning system** for the adaptive learning platform that:

✅ **Generates synthetic training data** - Realistic student learning patterns  
✅ **Trains neural network** - Predicts student performance (0-100 scale)  
✅ **Evaluates model** - MAE, RMSE, R² metrics  
✅ **Saves/loads models** - Persistent trained models  
✅ **Powers recommendations** - Intelligent course suggestions  

## Files Created

### Core ML Components
- `ml/training/data_generator.py` - Synthetic data generation
- `ml/training/adaptive_model.py` - Neural network model (5 inputs → 16 hidden → 1 output)
- `ml/training/training_pipeline.py` - Training orchestration + evaluation
- `ml/training/train.py` - Command-line training script
- `services/enhanced_adaptive_engine.py` - ML-powered adaptive engine
- `ml/AI_TRAINING_GUIDE.md` - Comprehensive documentation

## Quick Start (2 minutes)

```bash
# Navigate to backend
cd Backend/ml/training

# Install dependencies (if not already installed)
pip install numpy scikit-learn

# Train model (quick mode)
python train.py --quick

# Output: trained_models/adaptive_model_YYYYMMDD_HHMMSS.pkl
```

## Features

### 1. Predict Student Performance
```python
from services.enhanced_adaptive_engine import EnhancedAdaptiveEngine

engine = EnhancedAdaptiveEngine(model_path='ml/training/trained_models/adaptive_model.pkl')

prediction = engine.predict_performance(
    student_level=70,
    course_difficulty=75,
    engagement_score=0.8,
    learning_speed=1.2,
    time_spent_hours=10
)
# Returns: {'predicted_score': 78.5, 'confidence': 0.92, 'likely_completion': True}
```

### 2. Get Course Recommendations
```python
recommendations = engine.get_recommendations(
    user_id=1,
    user_level=70,
    engagement=0.8,
    learning_speed=1.2,
    available_courses=courses,
    limit=5
)
# Returns ranked list of recommended courses
```

### 3. Adjust Learning Difficulty
```python
adjustment = engine.adjust_learning_path(
    user_id=1,
    recent_performance=[75, 78, 82, 85]
)
# Suggests difficulty increase/decrease based on performance trend
```

### 4. Recommend Next Lesson
```python
next_lesson = engine.get_next_lesson(
    user_id=1,
    user_level=70,
    engagement=0.8,
    learning_speed=1.2,
    completed_lessons=[1, 2, 3],
    available_lessons=lessons
)
# Returns best next lesson for student
```

## Training Configuration

### Quick Training (2 minutes)
```bash
python train.py --quick
```
- 20 students, 500 interactions, 50 epochs

### Standard Training (5-10 minutes)
```bash
python train.py
```
- 100 students, 5000 interactions, 200 epochs

### Custom Training
```bash
python train.py --students 200 --interactions 10000 --epochs 300 --hidden-size 32
```

## Model Architecture

```
5 Input Features
    ↓
16 Hidden Neurons (ReLU)
    ↓
1 Output (Performance Score 0-100)
```

**Input Features:**
- Student Level (0-100)
- Course Difficulty (0-100)
- Engagement Score (0-1)
- Learning Speed (0.5-2.0)
- Time Spent (hours)

## Output & Metrics

After training, check `trained_models/results.json`:

```json
{
  "evaluation_metrics": {
    "mae": 8.5,        // Average error: 8.5 points
    "rmse": 10.2,      // Root mean squared error
    "r_squared": 0.92  // Explains 92% of variance
  }
}
```

## Integration with API

Update your route handler to use the model:

```python
from services.enhanced_adaptive_engine import EnhancedAdaptiveEngine

engine = EnhancedAdaptiveEngine('ml/training/trained_models/adaptive_model.pkl')

@router.get("/api/ai/recommendations/{user_id}")
async def recommend_courses(user_id: int):
    user = await get_user(user_id)
    courses = await get_courses()
    
    recommendations = engine.get_recommendations(
        user_id=user_id,
        user_level=user.learning_level,
        engagement=user.engagement_score,
        learning_speed=user.learning_speed,
        available_courses=courses
    )
    return {"recommendations": recommendations}
```

## Next Steps

1. **Train the model**: `python train.py --quick`
2. **Integrate with API**: Use `EnhancedAdaptiveEngine` in your routes
3. **Collect real data**: Track actual student performance to improve model
4. **Fine-tune**: Retrain with real data as you collect it
5. **Monitor**: Check metrics in `results.json` after each training

## File Structure

```
Backend/
├── ml/
│   ├── training/
│   │   ├── __init__.py
│   │   ├── data_generator.py      # Generate training data
│   │   ├── adaptive_model.py      # Neural network model
│   │   ├── training_pipeline.py   # Training orchestration
│   │   ├── train.py              # Main training script
│   │   └── trained_models/       # Saved models (generated after training)
│   │       ├── adaptive_model_*.pkl
│   │       ├── training_data.json
│   │       └── results.json
│   ├── AI_TRAINING_GUIDE.md      # Detailed documentation
│   └── recommendation_model.py
│
└── services/
    ├── enhanced_adaptive_engine.py # ML-powered recommendations
    ├── adaptive_engine.py
    ├── ai_solver.py
    └── ...
```

## Key Algorithms

### 1. Performance Prediction
Neural network learns relationship between:
- Student ability + Course difficulty → Expected performance
- Takes into account engagement and learning speed

### 2. Recommendation Scoring
```
score = performance (40%) + difficulty alignment (40%) + confidence (20%)
```
Balances: student will do well, course is appropriately challenging, prediction is reliable

### 3. Adaptive Difficulty Adjustment
- **Excellent (>80%)**: Increase difficulty (+15%)
- **Good (50-80%)**: Maintain or adjust (+10%)
- **Struggling (<50%)**: Decrease difficulty (-20%)

## Troubleshooting

**Error: numpy not found**
```bash
pip install numpy scikit-learn
```

**Error: Module not found**
- Make sure you're in `Backend/ml/training` directory
- Check Python path is set correctly

**Poor model performance?**
- Train with more data: `--interactions 10000`
- Use larger model: `--hidden-size 32`
- Train longer: `--epochs 500`

## Documentation

See **`ml/AI_TRAINING_GUIDE.md`** for:
- Detailed architecture explanation
- Advanced usage and customization
- Integration examples
- Performance tuning tips
- Future enhancement ideas

---

**Created:** January 24, 2026  
**Status:** Ready for training and integration ✅
