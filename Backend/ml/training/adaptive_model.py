"""
Adaptive Learning Neural Network Model
Predicts student performance and recommends optimal learning paths
"""
import numpy as np
from typing import Tuple, List, Dict, Optional
import pickle
import json
from pathlib import Path
from datetime import datetime


class AdaptiveLearningModel:
    """
    Neural network-based adaptive learning model
    Predicts student performance and provides personalized recommendations
    """
    
    def __init__(self, 
                 input_size: int = 5,
                 hidden_size: int = 16,
                 learning_rate: float = 0.01,
                 random_seed: int = 42):
        """
        Initialize the neural network model
        
        Args:
            input_size: Number of input features
            hidden_size: Number of hidden layer neurons
            learning_rate: Learning rate for training
            random_seed: Random seed for reproducibility
        """
        np.random.seed(random_seed)
        
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.learning_rate = learning_rate
        self.trained = False
        self.training_history = []
        
        # Initialize weights and biases
        self.W1 = np.random.randn(input_size, hidden_size) * 0.01
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, 1) * 0.01
        self.b2 = np.zeros((1, 1))
        
        # For tracking training
        self.loss_history = []
    
    @staticmethod
    def relu(z):
        """ReLU activation function"""
        return np.maximum(0, z)
    
    @staticmethod
    def relu_derivative(z):
        """Derivative of ReLU"""
        return (z > 0).astype(float)
    
    @staticmethod
    def sigmoid(z):
        """Sigmoid activation function (for output)"""
        return 1 / (1 + np.exp(-np.clip(z, -500, 500)))
    
    def forward(self, X: np.ndarray) -> Tuple[np.ndarray, dict]:
        """
        Forward pass through the network
        
        Args:
            X: Input features (batch_size, input_size)
            
        Returns:
            Tuple of (predictions, cache for backward pass)
        """
        # Hidden layer
        Z1 = np.dot(X, self.W1) + self.b1
        A1 = self.relu(Z1)
        
        # Output layer
        Z2 = np.dot(A1, self.W2) + self.b2
        A2 = Z2  # Linear output for regression
        
        cache = {'X': X, 'Z1': Z1, 'A1': A1, 'Z2': Z2, 'A2': A2}
        return A2, cache
    
    def compute_loss(self, y_pred: np.ndarray, y_true: np.ndarray) -> float:
        """Compute Mean Squared Error loss"""
        m = y_true.shape[0]
        loss = np.sum((y_pred - y_true) ** 2) / (2 * m)
        return loss
    
    def backward(self, cache: dict, y_true: np.ndarray) -> None:
        """
        Backward pass - compute gradients
        
        Args:
            cache: Cache from forward pass
            y_true: True labels
        """
        m = y_true.shape[0]
        
        X = cache['X']
        A1 = cache['A1']
        A2 = cache['A2']
        Z1 = cache['Z1']
        
        # Output layer gradient
        dZ2 = (A2 - y_true) / m
        dW2 = np.dot(A1.T, dZ2)
        db2 = np.sum(dZ2, axis=0, keepdims=True)
        
        # Hidden layer gradient
        dA1 = np.dot(dZ2, self.W2.T)
        dZ1 = dA1 * self.relu_derivative(Z1)
        dW1 = np.dot(X.T, dZ1)
        db1 = np.sum(dZ1, axis=0, keepdims=True)
        
        # Update weights
        self.W2 -= self.learning_rate * dW2
        self.b2 -= self.learning_rate * db2
        self.W1 -= self.learning_rate * dW1
        self.b1 -= self.learning_rate * db1
    
    def train(self, X: np.ndarray, y: np.ndarray, 
              epochs: int = 100, batch_size: int = 32, 
              validation_split: float = 0.2, verbose: bool = True) -> Dict:
        """
        Train the model
        
        Args:
            X: Training features
            y: Training labels
            epochs: Number of training epochs
            batch_size: Batch size for training
            validation_split: Fraction of data to use for validation
            verbose: Whether to print training progress
            
        Returns:
            Dictionary with training metrics
        """
        # Normalize inputs
        X_mean = np.mean(X, axis=0)
        X_std = np.std(X, axis=0) + 1e-8
        X_normalized = (X - X_mean) / X_std
        
        # Normalize outputs
        y_mean = np.mean(y)
        y_std = np.std(y)
        y_normalized = (y - y_mean) / y_std
        y_normalized = y_normalized.reshape(-1, 1)
        
        # Split into train/validation
        num_samples = X_normalized.shape[0]
        num_val = int(num_samples * validation_split)
        
        indices = np.random.permutation(num_samples)
        val_indices = indices[:num_val]
        train_indices = indices[num_val:]
        
        X_train, X_val = X_normalized[train_indices], X_normalized[val_indices]
        y_train, y_val = y_normalized[train_indices], y_normalized[val_indices]
        
        # Store normalization parameters
        self.X_mean = X_mean
        self.X_std = X_std
        self.y_mean = y_mean
        self.y_std = y_std
        
        # Training loop
        best_val_loss = float('inf')
        patience = 10
        patience_counter = 0
        
        for epoch in range(epochs):
            # Shuffle training data
            indices = np.random.permutation(X_train.shape[0])
            X_train_shuffled = X_train[indices]
            y_train_shuffled = y_train[indices]
            
            # Mini-batch training
            for i in range(0, X_train.shape[0], batch_size):
                X_batch = X_train_shuffled[i:i+batch_size]
                y_batch = y_train_shuffled[i:i+batch_size]
                
                y_pred, cache = self.forward(X_batch)
                self.backward(cache, y_batch)
            
            # Compute loss
            y_train_pred, _ = self.forward(X_train)
            train_loss = self.compute_loss(y_train_pred, y_train)
            
            y_val_pred, _ = self.forward(X_val)
            val_loss = self.compute_loss(y_val_pred, y_val)
            
            self.loss_history.append({'epoch': epoch, 'train_loss': train_loss, 'val_loss': val_loss})
            
            if verbose and (epoch + 1) % 10 == 0:
                print(f"Epoch {epoch + 1}/{epochs} - Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}")
            
            # Early stopping
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                patience_counter = 0
            else:
                patience_counter += 1
                if patience_counter >= patience:
                    if verbose:
                        print(f"Early stopping at epoch {epoch + 1}")
                    break
        
        self.trained = True
        return {
            'final_train_loss': train_loss,
            'final_val_loss': val_loss,
            'epochs_trained': len(self.loss_history),
            'best_val_loss': best_val_loss
        }
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions on new data
        
        Args:
            X: Input features
            
        Returns:
            Predicted performance scores
        """
        if not self.trained:
            raise ValueError("Model must be trained before making predictions")
        
        # Normalize using training statistics
        X_normalized = (X - self.X_mean) / self.X_std
        
        # Forward pass
        y_pred_normalized, _ = self.forward(X_normalized)
        
        # Denormalize predictions
        y_pred = y_pred_normalized * self.y_std + self.y_mean
        
        return np.clip(y_pred, 0, 100).flatten()
    
    def save_model(self, filepath: str) -> None:
        """Save model to file"""
        model_data = {
            'W1': self.W1,
            'b1': self.b1,
            'W2': self.W2,
            'b2': self.b2,
            'input_size': self.input_size,
            'hidden_size': self.hidden_size,
            'learning_rate': self.learning_rate,
            'trained': self.trained,
            'X_mean': self.X_mean,
            'X_std': self.X_std,
            'y_mean': self.y_mean,
            'y_std': self.y_std,
            'timestamp': datetime.now().isoformat()
        }
        
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
    
    def load_model(self, filepath: str) -> None:
        """Load model from file"""
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        self.W1 = model_data['W1']
        self.b1 = model_data['b1']
        self.W2 = model_data['W2']
        self.b2 = model_data['b2']
        self.input_size = model_data['input_size']
        self.hidden_size = model_data['hidden_size']
        self.learning_rate = model_data['learning_rate']
        self.trained = model_data['trained']
        self.X_mean = model_data['X_mean']
        self.X_std = model_data['X_std']
        self.y_mean = model_data['y_mean']
        self.y_std = model_data['y_std']
    
    def get_model_info(self) -> Dict:
        """Get model information"""
        return {
            'architecture': f"{self.input_size} -> {self.hidden_size} -> 1",
            'trained': self.trained,
            'learning_rate': self.learning_rate,
            'parameters': (self.input_size * self.hidden_size + self.hidden_size + 
                          self.hidden_size + 1),
        }
