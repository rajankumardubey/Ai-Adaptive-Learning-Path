from fastapi import UploadFile
import pytesseract
from PIL import Image
import io

class ImageProcessor:
    """Service for processing images (OCR, extraction, etc.)"""
    
    def __init__(self):
        pass
    
    async def process_image(self, image: UploadFile) -> str:
        """Extract text from image using OCR"""
        try:
            # Read image
            contents = await image.read()
            image_data = Image.open(io.BytesIO(contents))
            
            # Extract text using Tesseract
            text = pytesseract.image_to_string(image_data)
            return text
        except Exception as e:
            return f"Error processing image: {str(e)}"
    
    async def process_multiple_images(self, images: list) -> list:
        """Process multiple images"""
        results = []
        for image in images:
            text = await self.process_image(image)
            results.append(text)
        return results
    
    def validate_image(self, image: UploadFile) -> bool:
        """Validate if file is a valid image"""
        allowed_types = {"image/jpeg", "image/png", "image/gif", "image/webp"}
        return image.content_type in allowed_types
