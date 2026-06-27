#!/usr/bin/env python3
"""
Verification Script - Check that all AI system components are properly installed
Run this to verify everything is in place before training
"""

import os
import sys
from pathlib import Path

def check_file(path, name):
    """Check if a file exists"""
    if Path(path).exists():
        size = Path(path).stat().st_size
        print(f"  ✓ {name} ({size:,} bytes)")
        return True
    else:
        print(f"  ✗ {name} - NOT FOUND")
        return False

def check_directory(path, name):
    """Check if a directory exists"""
    if Path(path).exists():
        files = len(list(Path(path).glob('*')))
        print(f"  ✓ {name} ({files} files)")
        return True
    else:
        print(f"  ✗ {name} - NOT FOUND")
        return False

def verify_system():
    """Verify all components are in place"""
    
    print("\n" + "="*70)
    print("AI ADAPTIVE LEARNING SYSTEM - VERIFICATION")
    print("="*70 + "\n")
    
    base_path = Path(__file__).parent / "Backend"
    checks_passed = 0
    checks_total = 0
    
    # Check core training files
    print("🔍 Checking Core ML Components:")
    print("-" * 70)
    
    training_files = [
        ("ml/training/data_generator.py", "Data Generator"),
        ("ml/training/adaptive_model.py", "Adaptive Model"),
        ("ml/training/training_pipeline.py", "Training Pipeline"),
        ("ml/training/train.py", "Training Script"),
        ("ml/training/example_usage.py", "Example Usage"),
    ]
    
    for file_path, name in training_files:
        full_path = base_path / file_path
        checks_total += 1
        if check_file(full_path, name):
            checks_passed += 1
    
    # Check services
    print("\n🔍 Checking Services:")
    print("-" * 70)
    
    service_files = [
        ("services/enhanced_adaptive_engine.py", "Enhanced Adaptive Engine"),
    ]
    
    for file_path, name in service_files:
        full_path = base_path / file_path
        checks_total += 1
        if check_file(full_path, name):
            checks_passed += 1
    
    # Check documentation
    print("\n📖 Checking Documentation:")
    print("-" * 70)
    
    doc_files = [
        ("ml/QUICKSTART.md", "Quick Start Guide"),
        ("ml/AI_TRAINING_GUIDE.md", "Technical Guide"),
        ("AI_SYSTEM_SUMMARY.md", "System Summary"),
        ("IMPLEMENTATION_CHECKLIST.md", "Implementation Checklist"),
    ]
    
    for file_path, name in doc_files:
        full_path = base_path / file_path
        checks_total += 1
        if check_file(full_path, name):
            checks_passed += 1
    
    # Check API examples
    print("\n🔗 Checking API Integration:")
    print("-" * 70)
    
    api_files = [
        ("routes/ai_routes_examples.py", "API Routes Examples"),
    ]
    
    for file_path, name in api_files:
        full_path = base_path / file_path
        checks_total += 1
        if check_file(full_path, name):
            checks_passed += 1
    
    # Check directories
    print("\n📁 Checking Directories:")
    print("-" * 70)
    
    directories = [
        ("ml/training", "Training Directory"),
    ]
    
    for dir_path, name in directories:
        full_path = base_path / dir_path
        checks_total += 1
        if check_directory(full_path, name):
            checks_passed += 1
    
    # Summary
    print("\n" + "="*70)
    print("VERIFICATION SUMMARY")
    print("="*70)
    print(f"\nChecks Passed: {checks_passed}/{checks_total}")
    
    if checks_passed == checks_total:
        print("\n✅ ALL COMPONENTS VERIFIED - System is ready!\n")
        print("Next steps:")
        print("  1. cd Backend/ml/training")
        print("  2. python train.py --quick")
        print("  3. Check trained_models/results.json for metrics")
        print("  4. Follow IMPLEMENTATION_CHECKLIST.md for API integration\n")
        return True
    else:
        print(f"\n⚠️  MISSING {checks_total - checks_passed} COMPONENT(S)")
        print("Please ensure all files have been created properly.\n")
        return False

if __name__ == "__main__":
    success = verify_system()
    sys.exit(0 if success else 1)
