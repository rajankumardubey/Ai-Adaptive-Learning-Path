# Architecture Diagram & Data Flow

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ADAPTIVE LEARNING SYSTEM ARCHITECTURE                     │
└─────────────────────────────────────────────────────────────────────────────┘

DATA GENERATION LAYER
═════════════════════════════════════════════════════════════════════════════
  
  ┌──────────────────────────────────────────────────────────────────────┐
  │ TrainingDataGenerator (data_generator.py)                           │
  ├──────────────────────────────────────────────────────────────────────┤
  │ • generate_student_profiles(n_students)                             │
  │   → 100+ student profiles with:                                     │
  │     - initial_level (0-100)                                         │
  │     - learning_speed (0.5-2.0)                                      │
  │     - engagement (0.3-1.0)                                          │
  │     - subject_preference (Math/Science/Language/History)            │
  │     - learning_style (visual/auditory/kinesthetic/reading)          │
  │                                                                      │
  │ • generate_learning_interactions(n_interactions, n_students)        │
  │   → 5000+ realistic learning events with:                           │
  │     - student_id, course_id, timestamp                              │
  │     - engagement_score, learning_speed                              │
  │     - time_spent_hours, performance_score                           │
  │     - completed (bool)                                              │
  │                                                                      │
  │ • generate_feature_matrix() → (X, y)                                │
  │   → Feature vectors ready for training                              │
  └──────────────────────────────────────────────────────────────────────┘

MODEL TRAINING LAYER
═════════════════════════════════════════════════════════════════════════════

  ┌──────────────────────────────────────────────────────────────────────┐
  │ AdaptiveLearningModel (adaptive_model.py)                           │
  ├──────────────────────────────────────────────────────────────────────┤
  │ ARCHITECTURE:                                                        │
  │                                                                      │
  │  Input Features (5)                                                 │
  │    ├─ Student Level (0-100)                                         │
  │    ├─ Course Difficulty (0-100)                                     │
  │    ├─ Engagement Score (0-1)                                        │
  │    ├─ Learning Speed (0.5-2.0)                                      │
  │    └─ Time Spent (hours)                                            │
  │    │                                                                │
  │    ▼                                                                │
  │  Hidden Layer: 16 ReLU neurons                                      │
  │    │                                                                │
  │    ├─ Weights: 5×16 = 80                                            │
  │    ├─ Biases: 16                                                    │
  │    └─ Activation: ReLU (max(0, z))                                  │
  │    │                                                                │
  │    ▼                                                                │
  │  Output Layer: 1 neuron (Linear)                                    │
  │    │                                                                │
  │    ├─ Weights: 16×1 = 16                                            │
  │    ├─ Biases: 1                                                     │
  │    └─ Output: Performance Score (0-100)                             │
  │                                                                      │
  │ TRAINING ALGORITHM:                                                 │
  │ • Backpropagation (batch size: 32)                                  │
  │ • Learning rate: 0.01 (adaptive)                                    │
  │ • Loss function: Mean Squared Error (MSE)                           │
  │ • Epochs: 200 (with early stopping)                                 │
  │ • Validation split: 20%                                             │
  │                                                                      │
  │ PERFORMANCE MONITORING:                                             │
  │ • Training loss tracking                                            │
  │ • Validation loss tracking                                          │
  │ • Early stopping (patience=10)                                      │
  │ • Save best model                                                   │
  └──────────────────────────────────────────────────────────────────────┘

TRAINING PIPELINE LAYER
═════════════════════════════════════════════════════════════════════════════

  ┌──────────────────────────────────────────────────────────────────────┐
  │ TrainingPipeline (training_pipeline.py)                             │
  ├──────────────────────────────────────────────────────────────────────┤
  │                                                                      │
  │  Step 1: Data Generation                                            │
  │  ├─ Generate student profiles                                       │
  │  ├─ Generate learning interactions                                  │
  │  └─ Create feature matrices (X, y)                                  │
  │       │                                                             │
  │  Step 2: Model Creation                                             │
  │  └─ Initialize neural network (5-16-1)                              │
  │       │                                                             │
  │  Step 3: Model Training                                             │
  │  ├─ Split data (80/20 train/val)                                    │
  │  ├─ Train for N epochs                                              │
  │  ├─ Monitor loss and validation                                     │
  │  └─ Early stopping if no improvement                                │
  │       │                                                             │
  │  Step 4: Model Evaluation                                           │
  │  ├─ Test on hold-out set                                            │
  │  ├─ Calculate metrics (MAE, RMSE, R²)                               │
  │  ├─ Generate evaluation report                                      │
  │  └─ Save results.json                                               │
  │       │                                                             │
  │  Step 5: Model Persistence                                          │
  │  ├─ Save trained model (adaptive_model_*.pkl)                       │
  │  ├─ Save training data (training_data.json)                         │
  │  └─ Save results (results.json)                                     │
  │                                                                      │
  └──────────────────────────────────────────────────────────────────────┘

INFERENCE & RECOMMENDATION LAYER
═════════════════════════════════════════════════════════════════════════════

  ┌──────────────────────────────────────────────────────────────────────┐
  │ EnhancedAdaptiveEngine (enhanced_adaptive_engine.py)                │
  ├──────────────────────────────────────────────────────────────────────┤
  │                                                                      │
  │ Core Functions:                                                     │
  │                                                                      │
  │ 1. predict_performance()                                            │
  │    Input: Student profile + Course info                             │
  │    Process: Forward pass through NN                                 │
  │    Output: {predicted_score, confidence, likely_completion}         │
  │                                                                      │
  │ 2. get_recommendations()                                            │
  │    Input: Student profile + Available courses                       │
  │    Process:                                                         │
  │      ├─ Predict performance for each course                         │
  │      ├─ Calculate alignment score                                   │
  │      ├─ Combine: perf(40%) + align(40%) + conf(20%)                 │
  │      └─ Sort and return top-k                                       │
  │    Output: Ranked list of recommended courses                       │
  │                                                                      │
  │ 3. adjust_learning_path()                                           │
  │    Input: Recent performance scores                                 │
  │    Process:                                                         │
  │      ├─ Calculate average performance                               │
  │      ├─ Calculate performance trend (slope)                         │
  │      ├─ Determine action: INCREASE/DECREASE/MAINTAIN                │
  │      └─ Suggest specific adjustment amount                          │
  │    Output: {adjustment, recommendation, action}                     │
  │                                                                      │
  │ 4. get_next_lesson()                                                │
  │    Input: Student profile + Available lessons                       │
  │    Process:                                                         │
  │      ├─ Filter uncompleted lessons                                  │
  │      ├─ Predict performance on each                                 │
  │      ├─ Score by: perf(50%) + difficulty_bonus(50%)                 │
  │      └─ Return highest-scored lesson                                │
  │    Output: Recommended next lesson                                  │
  │                                                                      │
  └──────────────────────────────────────────────────────────────────────┘

API INTEGRATION LAYER
═════════════════════════════════════════════════════════════════════════════

  ┌──────────────────────────────────────────────────────────────────────┐
  │ FastAPI Routes (ai_routes_examples.py)                              │
  ├──────────────────────────────────────────────────────────────────────┤
  │                                                                      │
  │ POST /api/ai/predictions/performance                                │
  │   ├─ Input: {student_level, course_difficulty, ...}                │
  │   ├─ Call: engine.predict_performance()                             │
  │   └─ Output: {predicted_score, confidence, ...}                     │
  │                                                                      │
  │ GET /api/ai/recommendations/{user_id}                               │
  │   ├─ Input: user_id, limit=5                                        │
  │   ├─ Fetch: user data, available courses                            │
  │   ├─ Call: engine.get_recommendations()                             │
  │   └─ Output: [recommended courses]                                  │
  │                                                                      │
  │ POST /api/ai/difficulty/adjust/{user_id}                            │
  │   ├─ Input: {recent_performance: [scores]}                          │
  │   ├─ Call: engine.adjust_learning_path()                            │
  │   └─ Output: {adjustment, recommendation, action}                   │
  │                                                                      │
  │ GET /api/ai/recommendations/{user_id}/next-lesson                   │
  │   ├─ Input: user_id                                                 │
  │   ├─ Call: engine.get_next_lesson()                                 │
  │   └─ Output: {lesson_id, difficulty_score, ...}                     │
  │                                                                      │
  │ GET /api/ai/model/status                                            │
  │   └─ Output: Model load status, architecture, ...                   │
  │                                                                      │
  │ POST /api/ai/batch/predictions                                      │
  │   ├─ Input: [{student_level, ...}, ...]                             │
  │   └─ Output: [{prediction}, ...]                                    │
  │                                                                      │
  └──────────────────────────────────────────────────────────────────────┘

DATABASE LAYER
═════════════════════════════════════════════════════════════════════════════

  ┌──────────────────────────────────────────────────────────────────────┐
  │ Your Database (to be integrated)                                    │
  ├──────────────────────────────────────────────────────────────────────┤
  │                                                                      │
  │ Users Table                                                         │
  │ ├─ id, email, username                                              │
  │ ├─ learning_level (0-100) ← Used by AI                              │
  │ ├─ engagement_score (0-1) ← Used by AI                              │
  │ └─ learning_speed (0.5-2.0) ← Used by AI                            │
  │                                                                      │
  │ Courses Table                                                       │
  │ ├─ id, title, subject                                               │
  │ ├─ difficulty (Beginner/Intermediate/Advanced)                      │
  │ ├─ difficulty_score (0-100) ← Used by AI                            │
  │ └─ duration_hours ← Used by AI                                      │
  │                                                                      │
  │ Lessons Table                                                       │
  │ ├─ id, course_id, title                                             │
  │ ├─ difficulty_score (0-100) ← Used by AI                            │
  │ └─ duration_hours ← Used by AI                                      │
  │                                                                      │
  │ Progress Table                                                      │
  │ ├─ id, user_id, course_id                                           │
  │ ├─ completion_percentage                                            │
  │ ├─ score (0-100) ← Used for training                                │
  │ └─ completed (bool)                                                 │
  │                                                                      │
  └──────────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
┌─────────────────┐
│  Training Data  │
│   (Synthetic)   │
└────────┬────────┘
         │
         ▼
    ┌─────────┐
    │  Train  │──────────────┐
    │  Model  │              │
    └─────────┘              │
         │                   │
         ▼                   ▼
    ┌─────────┐         ┌──────────┐
    │ Trained │         │ Evaluate │
    │  Model  │◄────────│ Metrics  │
    └────┬────┘         └──────────┘
         │
         ├──────────────────────────────────────┐
         │                                      │
         ▼                                      ▼
    ┌─────────────┐             ┌──────────────────────┐
    │   Save to   │             │ Real Student Data    │
    │  Database   │             │ (for future retrng)  │
    └────┬────────┘             └─────────┬────────────┘
         │                               │
         ▼                               │
    ┌─────────────────────┐              │
    │ Load Trained Model  │              │
    └────┬────────────────┘              │
         │                               │
         ▼                               │
    ┌──────────────────────────────────┐ │
    │  Inference Engine                │ │
    │  (predict, recommend, adjust)    │ │
    └───┬──────────────────┬───────┬───┘ │
        │                  │       │     │
        ▼                  ▼       ▼     │
    ┌────────┐      ┌──────────┐ ┌─┐   │
    │ API    │      │ Dashboard│ │UI├───┘
    │Routes  │      │ Analytics│ └─┘
    └────────┘      └──────────┘
        │
        ▼
    ┌──────────────┐
    │  Frontend    │
    │  (Display)   │
    └──────────────┘
```

## Training Workflow

```
START
  │
  ├─→ Generate Data
  │   ├─ 100 student profiles
  │   ├─ 5000 interactions
  │   └─ Feature matrix (X, y)
  │
  ├─→ Split Data
  │   ├─ 80% training
  │   └─ 20% validation
  │
  ├─→ Initialize Model
  │   └─ 5 → 16 → 1 architecture
  │
  ├─→ Training Loop (200 epochs)
  │   ├─ Forward pass
  │   ├─ Compute loss
  │   ├─ Backward pass
  │   ├─ Update weights
  │   └─ Check early stopping?
  │       ├─ NO → Continue
  │       └─ YES → Stop
  │
  ├─→ Evaluate
  │   ├─ Predict on test set
  │   ├─ Calculate metrics
  │   │  ├─ MAE
  │   │  ├─ RMSE
  │   │  └─ R²
  │   └─ Generate report
  │
  ├─→ Save Model
  │   ├─ Save weights/biases
  │   ├─ Save training data
  │   └─ Save results.json
  │
  └─→ END (Model ready for inference)
```

## Prediction Workflow

```
START (New Student Request)
  │
  ├─→ Fetch Student Data
  │   ├─ learning_level
  │   ├─ engagement_score
  │   └─ learning_speed
  │
  ├─→ Fetch Course Data
  │   ├─ difficulty_score
  │   └─ duration_hours
  │
  ├─→ Load Trained Model
  │   └─ Forward pass
  │
  ├─→ Predict Performance
  │   ├─ Normalize input
  │   ├─ Forward pass
  │   ├─ Denormalize output
  │   └─ Calculate confidence
  │
  ├─→ Return Result
  │   ├─ predicted_score
  │   ├─ confidence
  │   └─ likely_completion
  │
  └─→ END (Display to user)
```

## Recommendation Ranking

```
STEP 1: Filter & Score Each Course
─────────────────────────────────────
  For each course:
    ├─ Predict performance → score_perf (0-100)
    ├─ Calculate difficulty alignment
    │  └─ alignment = 1 - |student_level - course_difficulty| / 100
    ├─ Get prediction confidence
    │  └─ conf = (alignment * 0.5 + engagement * 0.5)
    │
    └─ Recommendation Score:
       = score_perf * 0.4 + alignment * 0.4 + conf * 0.2

STEP 2: Sort by Recommendation Score
─────────────────────────────────────
  All courses sorted descending by recommendation_score

STEP 3: Return Top-K Recommendations
─────────────────────────────────────
  Return highest-scored courses (default: top 5)

EXAMPLE:
  Course A: pred=80, align=0.9, conf=0.85 → score = 0.87 ✓ #1
  Course B: pred=75, align=0.7, conf=0.75 → score = 0.72 ✓ #2
  Course C: pred=65, align=0.5, conf=0.60 → score = 0.58 ✓ #3
```

## Files Generated During Training

```
trained_models/
├── adaptive_model_20240124_103000.pkl
│   └─ Binary file containing:
│      ├─ W1, b1 (hidden layer weights/biases)
│      ├─ W2, b2 (output layer weights/biases)
│      ├─ X_mean, X_std (feature normalization)
│      ├─ y_mean, y_std (target normalization)
│      └─ Training parameters
│
├── training_data.json
│   └─ Contains:
│      ├─ Student profiles (100)
│      └─ Learning interactions (5000)
│
└── results.json
    └─ Contains:
       ├─ Training metrics (loss values)
       ├─ Evaluation metrics (MAE, RMSE, R²)
       ├─ Model architecture info
       └─ Timestamp
```

---

This architecture supports:
- **Scalability**: Can train on larger datasets
- **Modularity**: Each component can be updated independently
- **Extensibility**: Easy to add new features
- **Reliability**: Error handling and fallback mechanisms
- **Monitoring**: Metrics tracking and reporting
