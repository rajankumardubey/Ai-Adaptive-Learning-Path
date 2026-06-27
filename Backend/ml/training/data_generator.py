"""
Generate synthetic training data for the adaptive learning model
"""
import numpy as np
import json
from typing import List, Tuple, Dict
from datetime import datetime, timedelta
import random

class TrainingDataGenerator:
    """Generate synthetic training data for model training"""
    
    # def __init__(self, seed: int = 42):
    #     random.seed(seed)
    #     np.random.seed(seed)
    #     self.student_profiles = []
    #     self.interactions = []
    
    def generate_student_profiles(self, num_students: int = 100) -> List[Dict]:
        """
        Generate synthetic student profiles
        
        Args:
            num_students: Number of student profiles to generate
            
        Returns:
            List of student profile dictionaries
        """
        profiles = []
        for i in range(num_students):
            profile = {
                'student_id': i + 1,
                'initial_level': np.random.uniform(0, 100),
                'learning_speed': np.random.uniform(0.5, 2.0),  # multiplier for learning rate
                'engagement': np.random.uniform(0.3, 1.0),      # 0-1 scale
                'subject_preference': random.choice(['Math', 'Science', 'Language', 'History']),
                'learning_style': random.choice(['visual', 'auditory', 'kinesthetic', 'reading']),
            }
            profiles.append(profile)
        
        self.student_profiles = profiles
        return profiles
    
    def generate_course_data(self, num_courses: int = 50) -> List[Dict]:
        """
        Generate synthetic course data
        
        Args:
            num_courses: Number of courses to generate
            
        Returns:
            List of course dictionaries
        """
        subjects = ['Math', 'Science', 'Language', 'History']
        difficulties = ['Beginner', 'Intermediate', 'Advanced', 'Expert']
        
        courses = []
        for i in range(num_courses):
            course = {
                'course_id': i + 1,
                'title': f'Course {i+1}',
                'subject': random.choice(subjects),
                'difficulty': random.choice(difficulties),
                'duration_hours': random.uniform(5, 50),
                'avg_rating': np.random.uniform(3.5, 5.0),
                'difficulty_score': np.random.uniform(0, 100),
            }
            courses.append(course)
        
        return courses
    
    def generate_learning_interactions(self, 
                                      num_interactions: int = 5000,
                                      num_students: int = 100) -> List[Dict]:
        """
        Generate synthetic learning interactions/outcomes
        
        Args:
            num_interactions: Total interactions to generate
            num_students: Number of students (for reference)
            
        Returns:
            List of interaction dictionaries
        """
        courses = self.generate_course_data(50)
        interactions = []
        
        base_date = datetime.now() - timedelta(days=180)
        
        for _ in range(num_interactions):
            student_id = np.random.randint(1, num_students + 1)
            student = next((p for p in self.student_profiles if p['student_id'] == student_id), None)
            
            if not student:
                continue
            
            course = random.choice(courses)
            
            # Simulate interaction with learning factors
            base_performance = student['initial_level']
            difficulty_penalty = abs(base_performance - course['difficulty_score']) / 100
            
            # Generate performance score influenced by various factors
            performance_score = (
                base_performance * 0.3 +
                (100 - difficulty_penalty * 100) * 0.4 +
                student['engagement'] * 100 * 0.3 +
                np.random.normal(0, 10)  # Random noise
            )
            performance_score = np.clip(performance_score, 0, 100)
            
            # Calculate completion time (influenced by learning speed)
            base_time = course['duration_hours']
            actual_time = base_time / student['learning_speed'] + np.random.normal(0, 2)
            actual_time = max(actual_time, 0.5)
            
            interaction = {
                'timestamp': base_date + timedelta(days=np.random.randint(0, 180)),
                'student_id': student_id,
                'course_id': course['course_id'],
                'course_difficulty': course['difficulty_score'],
                'student_level': base_performance,
                'engagement_score': student['engagement'],
                'learning_speed': student['learning_speed'],
                'time_spent_hours': actual_time,
                'performance_score': performance_score,
                'completed': performance_score > 50,
                'difficulty_rating': course['difficulty'],
                'completion_rate': min(performance_score / 100, 1.0),
            }
            interactions.append(interaction)
        
        self.interactions = interactions
        return interactions
    
    def generate_feature_matrix(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create feature matrix and labels from interactions
        
        Returns:
            Tuple of (features array, labels array)
        """
        if not self.interactions:
            raise ValueError("No interactions data. Generate interactions first.")
        
        X = []
        y = []
        
        for interaction in self.interactions:
            # Feature vector
            features = [
                interaction['student_level'],
                interaction['course_difficulty'],
                interaction['engagement_score'],
                interaction['learning_speed'],
                interaction['time_spent_hours'],
            ]
            X.append(features)
            
            # Label: performance score
            y.append(interaction['performance_score'])
        
        return np.array(X), np.array(y)
    
    def save_training_data(self, filepath: str):
        """Save training data to JSON file"""
        data = {
            'students': self.student_profiles,
            'interactions': [
                {k: (v.isoformat() if isinstance(v, datetime) else bool(v) if isinstance(v, (np.bool_, bool)) else v) 
                 for k, v in interaction.items()}
                for interaction in self.interactions
            ]
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    @staticmethod
    def load_training_data(filepath: str) -> Tuple[List[Dict], List[Dict]]:
        """Load training data from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return data['students'], data['interactions']
