import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

class RecommendationModel:
    """Deep learning model for content recommendations"""
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
    
    def get_embedding(self, text: str) -> np.ndarray:
        """Get embedding for text"""
        return self.model.encode(text)
    
    def recommend_content(self, user_profile: str, content_list: list, top_k: int = 5) -> list:
        """Recommend top-k content based on user profile"""
        user_embedding = self.get_embedding(user_profile)
        
        recommendations = []
        for content in content_list:
            content_embedding = self.get_embedding(content.get('description', ''))
            similarity = cosine_similarity([user_embedding], [content_embedding])[0][0]
            recommendations.append({
                'id': content.get('id'),
                'title': content.get('title'),
                'score': float(similarity),
                'description': content.get('description')
            })
        
        # Sort and return top-k
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:top_k]
    
    def get_similar_courses(self, course_id: int, all_courses: list, top_k: int = 5) -> list:
        """Get similar courses"""
        target_course = next((c for c in all_courses if c.get('id') == course_id), None)
        if not target_course:
            return []
        
        target_embedding = self.get_embedding(target_course.get('description', ''))
        
        similarities = []
        for course in all_courses:
            if course.get('id') == course_id:
                continue
            
            course_embedding = self.get_embedding(course.get('description', ''))
            similarity = cosine_similarity([target_embedding], [course_embedding])[0][0]
            similarities.append({
                'id': course.get('id'),
                'title': course.get('title'),
                'score': float(similarity)
            })
        
        similarities.sort(key=lambda x: x['score'], reverse=True)
        return similarities[:top_k]
