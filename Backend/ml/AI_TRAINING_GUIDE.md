# AI Model Training and Implementation Guide

## Overview

This document explains the AI adaptive learning system for the Adaptive Learning Path project. The system includes:

1. **Data Generation**: Synthetic training data generator simulating student learning patterns
2. **Neural Network Model**: Deep learning model for predicting student performance
3. **Training Pipeline**: End-to-end training orchestration
4. **Enhanced Adaptive Engine**: ML-powered recommendation system

## Architecture

### Model Architecture

```
Input Features (5)
    ↓
Hidden Layer (ReLU activation, configurable size)
    ↓
Output Layer (Linear, 0-100 scale)
```

**Input Features:**
- Student Level (0-100): Current learning proficiency
- Course Difficulty (0-100): Difficulty of the course
- Engagement Score (0-1): Student's engagement level
- Learning Speed (0.5-2.0): How quickly student learns
- Time Spent (hours): Time invested in learning

**Output:**
- Performance Score (0-100): Predicted performance on the course

### Key Components

#### 1. Data Generator (`ml/training/data_generator.py`)

Generates synthetic training data with realistic learning patterns:

```python
from training.data_generator import TrainingDataGenerator

generator = TrainingDataGenerator()
profiles = generator.generate_student_profiles(num_students=100)
interactions = generator.generate_learning_interactions(num_interactions=5000)
X, y = generator.generate_feature_matrix()
```

**Generated Data:**
- Student profiles with learning characteristics
- Learning interactions with realistic performance patterns
- Feature matrix ready for model training

#### 2. Adaptive Model (`ml/training/adaptive_model.py`)

Neural network implementation with:
- ReLU activation in hidden layer
- Linear output for regression
- Adam-style SGD optimization
- Early stopping and validation monitoring

```python
from training.adaptive_model import AdaptiveLearningModel

model = AdaptiveLearningModel(input_size=5, hidden_size=16, learning_rate=0.01)
model.train(X, y, epochs=200, batch_size=32, validation_split=0.2)

# Make predictions
predictions = model.predict(X_test)

# Save/load
model.save_model('models/my_model.pkl')
model.load_model('models/my_model.pkl')
```

#### 3. Training Pipeline (`ml/training/training_pipeline.py`)

Orchestrates the complete training process:

```python
from training.training_pipeline import TrainingPipeline

pipeline = TrainingPipeline(model_save_dir='trained_models')

# Run full pipeline
results = pipeline.full_pipeline(
    num_students=100,
    num_interactions=5000,
    epochs=200,
    batch_size=32,
    hidden_size=16
)
```

**Pipeline Steps:**
1. Generate synthetic training data
2. Create neural network model
3. Train model with validation
4. Evaluate on test set
5. Save trained model and results

#### 4. Enhanced Adaptive Engine (`services/enhanced_adaptive_engine.py`)

Uses trained model for intelligent recommendations:

```python
from services.enhanced_adaptive_engine import EnhancedAdaptiveEngine

engine = EnhancedAdaptiveEngine(model_path='trained_models/adaptive_model.pkl')

# Predict performance
prediction = engine.predict_performance(
    student_level=70,
    course_difficulty=75,
    engagement_score=0.8,
    learning_speed=1.2,
    time_spent_hours=10
)

# Get recommendations
recommendations = engine.get_recommendations(
    user_id=1,
    user_level=70,
    engagement=0.8,
    learning_speed=1.2,
    available_courses=courses,
    limit=5
)

# Adjust learning path
adjustment = engine.adjust_learning_path(
    user_id=1,
    recent_performance=[75, 78, 82, 85]
)
```

## Training Instructions

### Quick Start

1. **Navigate to training directory:**
```bash
cd Backend/ml/training
```

2. **Install dependencies:**
```bash
pip install numpy scikit-learn
```

3. **Run training (quick mode - ~2 minutes):**
```bash
python train.py --quick
```

4. **Run full training (~5-10 minutes):**
```bash
python train.py --students 100 --interactions 5000 --epochs 200
```

### Training Options

```bash
python train.py --help

Usage: train.py [OPTIONS]

Options:
  --students INTEGER        Number of synthetic students (default: 100)
  --interactions INTEGER    Number of learning interactions (default: 5000)
  --epochs INTEGER         Number of training epochs (default: 200)
  --batch-size INTEGER     Batch size (default: 32)
  --hidden-size INTEGER    Hidden layer size (default: 16)
  --model-dir TEXT        Directory to save models (default: trained_models)
  --quick                 Quick training mode (reduced dataset and epochs)
```

### Training Output

After training, you'll find in the `trained_models/` directory:

1. **adaptive_model_YYYYMMDD_HHMMSS.pkl**: Trained model file
2. **training_data.json**: Generated training data
3. **results.json**: Training and evaluation metrics

Example `results.json`:
```json
{
  "timestamp": "2024-01-24T10:30:00",
  "training_config": {
    "num_students": 100,
    "num_interactions": 5000,
    "epochs": 200,
    "batch_size": 32,
    "hidden_size": 16
  },
  "training_metrics": {
    "final_train_loss": 0.0234,
    "final_val_loss": 0.0245,
    "epochs_trained": 150
  },
  "evaluation_metrics": {
    "mae": 8.5,
    "rmse": 10.2,
    "r_squared": 0.92
  }
}
```

## Performance Metrics

The model is evaluated using standard regression metrics:

- **MAE (Mean Absolute Error)**: Average prediction error in points
  - Lower is better
  - Typical range: 5-15 points
  
- **RMSE (Root Mean Squared Error)**: Penalizes larger errors more heavily
  - Lower is better
  - Typical range: 8-20 points
  
- **R² Score**: Proportion of variance explained
  - Range: 0-1 (1 is perfect)
  - Target: > 0.85

## Integration with API

### Using the Model in Routes

```python
from services.enhanced_adaptive_engine import EnhancedAdaptiveEngine
from fastapi import APIRouter

router = APIRouter()
engine = EnhancedAdaptiveEngine(model_path='ml/training/trained_models/adaptive_model_latest.pkl')

@router.get("/recommendations/{user_id}")
async def get_recommendations(user_id: int, limit: int = 5):
    # Fetch user data from database
    user = get_user(user_id)
    courses = get_available_courses()
    
    # Get ML-powered recommendations
    recommendations = engine.get_recommendations(
        user_id=user_id,
        user_level=user.learning_level,
        engagement=user.engagement_score,
        learning_speed=user.learning_speed,
        available_courses=courses,
        limit=limit
    )
    
    return {"recommendations": recommendations}
```

## Troubleshooting

### Model Not Found Error
```
Error: Model file not found
Solution: Train the model first using: python train.py --quick
```

### Poor Performance Metrics
- Increase training data: `--interactions 10000`
- Increase model complexity: `--hidden-size 32`
- Train longer: `--epochs 500`

### Memory Issues
- Reduce batch size: `--batch-size 16`
- Reduce student count: `--students 50`
- Reduce interactions: `--interactions 2000`

## Advanced Usage

### Custom Model Architecture

```python
# Create custom model with different architecture
model = AdaptiveLearningModel(
    input_size=7,  # More features
    hidden_size=32,  # Larger hidden layer
    learning_rate=0.001  # Lower learning rate
)
```

### Fine-tuning on Real Data

```python
pipeline = TrainingPipeline()
pipeline.model = pipeline.create_model()

# Load real data from database
real_X, real_y = load_real_training_data()

# Fine-tune
metrics = pipeline.train_model(real_X, real_y, epochs=50)
```

## Model Versioning

Each training creates a timestamped model file:
- `adaptive_model_20240124_103000.pkl` - First training
- `adaptive_model_20240124_150000.pkl` - Second training (improved)

To use a specific model version:
```python
engine = EnhancedAdaptiveEngine(model_path='trained_models/adaptive_model_20240124_150000.pkl')
```

## Future Enhancements

1. **Multi-task Learning**: Predict multiple outcomes (performance, time, engagement)
2. **Attention Mechanisms**: Identify which features matter most for each student
3. **Online Learning**: Update model with real student data continuously
4. **Ensemble Models**: Combine multiple models for better predictions
5. **Feature Engineering**: Add domain-specific features from educational research

## References

- Student modeling and adaptive learning research
- Deep learning for education (Zhang et al., 2019)
- Learning analytics best practices

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review training logs in `trained_models/`
3. Verify all dependencies are installed
4. Check model performance metrics in `results.json`
