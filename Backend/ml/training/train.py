"""
Main training script to train the adaptive learning AI model
Run this script to generate training data and train the model
"""
import sys
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from training_pipeline import TrainingPipeline


def main():
    parser = argparse.ArgumentParser(description='Train Adaptive Learning Model')
    parser.add_argument('--students', type=int, default=100, help='Number of synthetic students')
    parser.add_argument('--interactions', type=int, default=5000, help='Number of learning interactions')
    parser.add_argument('--epochs', type=int, default=200, help='Number of training epochs')
    parser.add_argument('--batch-size', type=int, default=32, help='Batch size')
    parser.add_argument('--hidden-size', type=int, default=16, help='Hidden layer size')
    parser.add_argument('--model-dir', type=str, default='trained_models', help='Directory to save models')
    parser.add_argument('--quick', action='store_true', help='Quick training with smaller dataset')
    
    args = parser.parse_args()
    
    # Adjust settings for quick training
    if args.quick:
        args.students = 20
        args.interactions = 500
        args.epochs = 50
        print("\n Quick training mode: reduced dataset and epochs")
    
    pipeline = TrainingPipeline(model_save_dir=args.model_dir)
    
    results = pipeline.full_pipeline(
        num_students=args.students,
        num_interactions=args.interactions,
        epochs=args.epochs,
        batch_size=args.batch_size,
        hidden_size=args.hidden_size
    )
    
    print("\n" + "="*50)
    print("Training Summary:")
    print("="*50)
    print(f"Training Metrics:")
    for key, value in results['training_metrics'].items():
        print(f"  {key}: {value}")
    
    print(f"\nEvaluation Metrics:")
    for key, value in results['evaluation_metrics'].items():
        print(f"  {key}: {value:.4f}")
    
    print(f"\nModel Info:")
    for key, value in results['model_info'].items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
