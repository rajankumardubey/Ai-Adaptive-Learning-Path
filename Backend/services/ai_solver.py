from typing import Optional
import openai
from config import settings
from services.image_processor import ImageProcessor

class AIDoubSolver:
    """AI service for solving student doubts using LLM"""
    
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.image_processor = ImageProcessor()
    
    def solve(self, question: str, image_context: Optional[str] = None) -> dict:
        """Solve a student's doubt using AI"""
        context = question
        if image_context:
            context += f"\n\nImage context: {image_context}"
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert tutor helping students understand concepts."},
                    {"role": "user", "content": context}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            answer = response.choices[0].message.content
            
            return {
                "answer": answer,
                "steps": self._extract_steps(answer),
                "relatedTopics": self._get_related_topics(question),
                "confidence": 0.9
            }
        except Exception as e:
            return {
                "error": str(e),
                "answer": "Unable to process your question at this moment."
            }
    
    async def extract_text_from_image(self, image):
        """Extract text from uploaded image using OCR"""
        return await self.image_processor.process_image(image)
    
    def _extract_steps(self, answer: str) -> list:
        """Extract solution steps from answer"""
        # Parse answer to extract steps
        steps = answer.split('\n')
        return [step.strip() for step in steps if step.strip()]
    
    def _get_related_topics(self, question: str) -> list:
        """Get related learning topics"""
        # Simple keyword extraction
        related = ["Mathematics Basics", "Problem Solving"]
        return related
