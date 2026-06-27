"""
Model Training Pipeline
Orchestrates data generation, training, and evaluation
"""
import numpy as np
from typing import Dict, Tuple, Optional
from pathlib import Path
import json
from datetime import datetime

from data_generator import TrainingDataGenerator
from adaptive_model import AdaptiveLearningModel


class ModelEvaluator:
    """Evaluate model performance"""
    
    @staticmethod
    def mean_absolute_error(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calculate Mean Absolute Error"""
        return np.mean(np.abs(y_true - y_pred))
    
    @staticmethod
    def root_mean_squared_error(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calculate Root Mean Squared Error"""
        return np.sqrt(np.mean((y_true - y_pred) ** 2))
    
    @staticmethod
    def r_squared(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calculate R-squared score"""
        ss_res = np.sum((y_true - y_pred) ** 2)
        ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
        return 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
    
    @staticmethod
    def evaluate(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """
        Comprehensive model evaluation
        
        Args:
            y_true: True values
            y_pred: Predicted values
            
        Returns:
            Dictionary of metrics
        """
        return {
            'mae': ModelEvaluator.mean_absolute_error(y_true, y_pred),
            'rmse': ModelEvaluator.root_mean_squared_error(y_true, y_pred),
            'r_squared': ModelEvaluator.r_squared(y_true, y_pred),
        }


class TrainingPipeline:
    """Complete training pipeline"""
    
    def __init__(self, model_save_dir: str = "trained_models"):
        self.model_save_dir = Path(model_save_dir)
        self.model_save_dir.mkdir(parents=True, exist_ok=True)
        
        self.data_generator = None
        self.model = None
        self.training_config = None
        self.evaluation_results = None
    
    def generate_training_data(self, 
                              num_students: int = 100,
                              num_interactions: int = 5000,
                              save_data: bool = True) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate training data
        
        Args:
            num_students: Number of synthetic students
            num_interactions: Number of learning interactions
            save_data: Whether to save generated data
            
        Returns:
            Tuple of (features, labels)
        """
        print(f"Generating training data ({num_interactions} interactions from {num_students} students)...")
        
        self.data_generator = TrainingDataGenerator()
        self.data_generator.generate_student_profiles(num_students)
        self.data_generator.generate_learning_interactions(num_interactions, num_students)
        
        X, y = self.data_generator.generate_feature_matrix()
        
        if save_data:
            data_path = self.model_save_dir / "training_data.json"
            self.data_generator.save_training_data(str(data_path))
            print(f"Training data saved to {data_path}")
        
        print(f"Generated {X.shape[0]} training samples with {X.shape[1]} features")
        return X, y
    
    def create_model(self, 
                    input_size: int = 5,
                    hidden_size: int = 16,
                    learning_rate: float = 0.01) -> AdaptiveLearningModel:
        """
        Create a new model instance
        
        Args:
            input_size: Number of input features
            hidden_size: Number of hidden layer neurons
            learning_rate: Learning rate
            
        Returns:
            AdaptiveLearningModel instance
        """
        print(f"Creating model: {input_size} -> {hidden_size} -> 1")
        self.model = AdaptiveLearningModel(
            input_size=input_size,
            hidden_size=hidden_size,
            learning_rate=learning_rate
        )
        return self.model
    
    def train_model(self,
                   X: np.ndarray,
                   y: np.ndarray,
                   epochs: int = 100,
                   batch_size: int = 32,
                   validation_split: float = 0.2) -> Dict:
        """
        Train the model
        
        Args:
            X: Training features
            y: Training labels
            epochs: Number of training epochs
            batch_size: Batch size
            validation_split: Validation set split ratio
            
        Returns:
            Training metrics
        """
        if self.model is None:
            raise ValueError("Model not created. Call create_model() first.")
        
        print(f"Training model for {epochs} epochs...")
        training_metrics = self.model.train(
            X, y,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            verbose=True
        )
        
        return training_metrics
    
    def evaluate_model(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict:
        """
        Evaluate trained model
        
        Args:
            X_test: Test features
            y_test: Test labels
            
        Returns:
            Evaluation metrics
        """
        if self.model is None or not self.model.trained:
            raise ValueError("Model not trained. Train model first.")
        
        print("Evaluating model...")
        y_pred = self.model.predict(X_test)
        
        metrics = ModelEvaluator.evaluate(y_test, y_pred)
        self.evaluation_results = metrics
        
        print(f"Evaluation Results:")
        print(f"  MAE: {metrics['mae']:.4f}")
        print(f"  RMSE: {metrics['rmse']:.4f}")
        print(f"  R²: {metrics['r_squared']:.4f}")
        
        return metrics
    
    def full_pipeline(self,
                     num_students: int = 100,
                     num_interactions: int = 5000,
                     epochs: int = 100,
                     batch_size: int = 32,
                     hidden_size: int = 16) -> Dict:
        """
        Run complete training pipeline
        
        Args:
            num_students: Number of synthetic students
            num_interactions: Number of interactions
            epochs: Training epochs
            batch_size: Batch size
            hidden_size: Hidden layer size
            
        Returns:
            Complete results dictionary
        """
        print("\n" + "="*50)
        print("STARTING FULL TRAINING PIPELINE")
        print("="*50 + "\n")
        
        # Generate data
        X, y = self.generate_training_data(num_students, num_interactions)
        
        # Create model
        self.create_model(input_size=X.shape[1], hidden_size=hidden_size)
        
        # Train model
        training_metrics = self.train_model(X, y, epochs=epochs, batch_size=batch_size)
        print(f"\nTraining completed: {training_metrics}")
        
        # Split data for evaluation
        num_test = int(0.2 * X.shape[0])
        X_train, X_test = X[:-num_test], X[-num_test:]
        y_train, y_test = y[:-num_test], y[-num_test:]
        
        # Evaluate
        evaluation_metrics = self.evaluate_model(X_test, y_test)
        
        # Save model
        model_path = self._get_model_path()
        self.model.save_model(str(model_path))
        print(f"\nModel saved to {model_path}")
        
        # Save pipeline results
        results = {
            'timestamp': datetime.now().isoformat(),
            'training_config': {
                'num_students': num_students,
                'num_interactions': num_interactions,
                'epochs': epochs,
                'batch_size': batch_size,
                'hidden_size': hidden_size,
            },
            'training_metrics': training_metrics,
            'evaluation_metrics': evaluation_metrics,
            'model_info': self.model.get_model_info(),
        }
        
        results_path = self.model_save_dir / "results.json"
        with open(results_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print("\n" + "="*50)
        print("PIPELINE COMPLETED SUCCESSFULLY")
        print("="*50 + "\n")
        
        return results
    
    def _get_model_path(self) -> Path:
        """Generate model file path with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return self.model_save_dir / f"adaptive_model_{timestamp}.pkl"
    
    def load_and_evaluate(self, model_path: str, X_test: np.ndarray, y_test: np.ndarray):
        """Load a trained model and evaluate it"""
        print(f"Loading model from {model_path}...")
        self.model = AdaptiveLearningModel()
        self.model.load_model(model_path)
        
        print(f"Model loaded. Architecture: {self.model.get_model_info()}")
        
        return self.evaluate_model(X_test, y_test)


if __name__ == "__main__":
    # Example usage
    pipeline = TrainingPipeline()
    results = pipeline.full_pipeline(
        num_students=100,
        num_interactions=5000,
        epochs=200,
        batch_size=32,
        hidden_size=16
    )
    
    print("\nFinal Results:")
    print(json.dumps(results, indent=2))
