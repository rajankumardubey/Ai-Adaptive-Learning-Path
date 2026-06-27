"""
Example usage and testing script for the adaptive learning AI system
Demonstrates all key functionality
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from data_generator import TrainingDataGenerator
from adaptive_model import AdaptiveLearningModel
from training_pipeline import TrainingPipeline, ModelEvaluator
import numpy as np


def example_data_generation():
    """Example 1: Generate training data"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Data Generation")
    print("="*60)
    
    generator = TrainingDataGenerator(seed=42)
    
    # Generate student profiles
    students = generator.generate_student_profiles(num_students=10)
    print(f"\nGenerated {len(students)} student profiles")
    print(f"Sample student: {students[0]}")
    
    # Generate course data
    courses = generator.generate_course_data(num_courses=20)
    print(f"\nGenerated {len(courses)} courses")
    print(f"Sample course: {courses[0]}")
    
    # Generate interactions
    interactions = generator.generate_learning_interactions(
        num_interactions=500, 
        num_students=10
    )
    print(f"\nGenerated {len(interactions)} learning interactions")
    print(f"Sample interaction: {interactions[0]}")
    
    # Create feature matrix
    X, y = generator.generate_feature_matrix()
    print(f"\nFeature matrix shape: {X.shape}")
    print(f"Feature ranges:")
    print(f"  Student Level: {X[:, 0].min():.2f} - {X[:, 0].max():.2f}")
    print(f"  Course Difficulty: {X[:, 1].min():.2f} - {X[:, 1].max():.2f}")
    print(f"  Engagement: {X[:, 2].min():.2f} - {X[:, 2].max():.2f}")
    print(f"  Learning Speed: {X[:, 3].min():.2f} - {X[:, 3].max():.2f}")
    print(f"  Time Spent: {X[:, 4].min():.2f} - {X[:, 4].max():.2f}")
    print(f"  Performance scores: {y.min():.2f} - {y.max():.2f}")
    
    return X, y


def example_model_training(X, y):
    """Example 2: Train a model"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Model Training")
    print("="*60)
    
    # Create model
    model = AdaptiveLearningModel(
        input_size=X.shape[1],
        hidden_size=8,
        learning_rate=0.01
    )
    print(f"\nCreated model: {model.get_model_info()}")
    
    # Train model
    print("\nTraining model...")
    metrics = model.train(
        X, y,
        epochs=50,
        batch_size=16,
        validation_split=0.2,
        verbose=False
    )
    
    print(f"\nTraining completed:")
    print(f"  Final train loss: {metrics['final_train_loss']:.4f}")
    print(f"  Final validation loss: {metrics['final_val_loss']:.4f}")
    print(f"  Epochs trained: {metrics['epochs_trained']}")
    
    # Make predictions
    y_pred = model.predict(X[:10])
    print(f"\nSample predictions (first 10):")
    for i, (true_val, pred_val) in enumerate(zip(y[:10], y_pred)):
        error = abs(true_val - pred_val)
        print(f"  Sample {i+1}: True={true_val:.2f}, Pred={pred_val:.2f}, Error={error:.2f}")
    
    return model


def example_model_evaluation(model, X, y):
    """Example 3: Evaluate model"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Model Evaluation")
    print("="*60)
    
    # Split data
    num_test = max(1, int(0.2 * len(X)))
    X_test, y_test = X[-num_test:], y[-num_test:]
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Evaluate
    metrics = ModelEvaluator.evaluate(y_test, y_pred)
    
    print(f"\nEvaluation metrics on test set ({len(y_test)} samples):")
    print(f"  MAE (Mean Absolute Error): {metrics['mae']:.4f}")
    print(f"  RMSE (Root Mean Squared Error): {metrics['rmse']:.4f}")
    print(f"  R² Score: {metrics['r_squared']:.4f}")
    
    print(f"\nInterpretation:")
    if metrics['mae'] < 10:
        print(f"  ✓ Low error: Model predictions are typically within 10 points")
    if metrics['r_squared'] > 0.8:
        print(f"  ✓ Good fit: Model explains {metrics['r_squared']*100:.1f}% of variance")


def example_adaptive_engine():
    """Example 4: Use the adaptive engine"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Adaptive Engine Usage")
    print("="*60)
    
    from services.enhanced_adaptive_engine import EnhancedAdaptiveEngine
    
    # Create engine (without trained model - will use fallback estimation)
    engine = EnhancedAdaptiveEngine()
    
    print("\nExample: Predicting student performance")
    prediction = engine.predict_performance(
        student_level=70,
        course_difficulty=75,
        engagement_score=0.8,
        learning_speed=1.2,
        time_spent_hours=10
    )
    
    print(f"  Student Level: 70/100")
    print(f"  Course Difficulty: 75/100")
    print(f"  Engagement: 0.8/1.0")
    print(f"  Learning Speed: 1.2x")
    print(f"  Time Spent: 10 hours")
    print(f"\n  Prediction:")
    print(f"    Predicted Score: {prediction['predicted_score']:.2f}/100")
    print(f"    Confidence: {prediction['confidence']:.2%}")
    print(f"    Likely Completion: {prediction['likely_completion']}")
    print(f"    Model Used: {'ML Model' if prediction['model_used'] else 'Heuristic Fallback'}")
    
    # Example: Get recommendations
    print("\n\nExample: Course recommendations")
    courses = [
        {'id': 1, 'title': 'Python Basics', 'subject': 'CS', 'difficulty': 'Beginner', 
         'duration_hours': 10, 'difficulty_score': 30},
        {'id': 2, 'title': 'Advanced Python', 'subject': 'CS', 'difficulty': 'Intermediate',
         'duration_hours': 20, 'difficulty_score': 60},
        {'id': 3, 'title': 'Machine Learning', 'subject': 'CS', 'difficulty': 'Advanced',
         'duration_hours': 30, 'difficulty_score': 80},
        {'id': 4, 'title': 'Data Structures', 'subject': 'CS', 'difficulty': 'Intermediate',
         'duration_hours': 15, 'difficulty_score': 65},
        {'id': 5, 'title': 'Web Development', 'subject': 'CS', 'difficulty': 'Beginner',
         'duration_hours': 12, 'difficulty_score': 40},
    ]
    
    recommendations = engine.get_recommendations(
        user_id=1,
        user_level=70,
        engagement=0.8,
        learning_speed=1.2,
        available_courses=courses,
        limit=3
    )
    
    print(f"  Top 3 recommended courses for a student at level 70:")
    for i, rec in enumerate(recommendations, 1):
        print(f"\n  {i}. {rec['course_title']}")
        print(f"     Predicted Score: {rec['predicted_score']:.2f}/100")
        print(f"     Completion Likelihood: {rec['completion_likelihood']}")
        print(f"     Recommendation Score: {rec['recommendation_score']:.2%}")
    
    # Example: Adjust learning path
    print("\n\nExample: Adaptive difficulty adjustment")
    recent_performance = [55, 62, 68, 75, 82]
    
    adjustment = engine.adjust_learning_path(
        user_id=1,
        recent_performance=recent_performance
    )
    
    print(f"  Recent performance: {recent_performance}")
    print(f"  Average performance: {adjustment['average_performance']:.2f}/100")
    print(f"  Performance trend: {adjustment['performance_trend']:+.2f} points/session")
    print(f"  Recommended action: {adjustment['suggested_action']}")
    print(f"  Reason: {adjustment['recommendation']}")


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("AI ADAPTIVE LEARNING SYSTEM - EXAMPLES")
    print("="*60)
    
    try:
        # Example 1: Data Generation
        X, y = example_data_generation()
        
        # Example 2: Model Training
        model = example_model_training(X, y)
        
        # Example 3: Evaluation
        example_model_evaluation(model, X, y)
        
        # Example 4: Adaptive Engine
        try:
            example_adaptive_engine()
        except ImportError:
            print("\n(Skipped adaptive engine example - requires services module)")
        
        print("\n" + "="*60)
        print("EXAMPLES COMPLETED SUCCESSFULLY ✓")
        print("="*60)
        print("\nNext steps:")
        print("1. Run full training: python train.py --quick")
        print("2. Integrate with API using EnhancedAdaptiveEngine")
        print("3. See ml/QUICKSTART.md and ml/AI_TRAINING_GUIDE.md for more info")
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
