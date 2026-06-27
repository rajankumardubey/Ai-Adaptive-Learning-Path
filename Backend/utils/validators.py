from typing import Any, Dict

class ValidationError(Exception):
    """Custom validation error"""
    pass

def validate_required_fields(data: Dict, required_fields: list) -> bool:
    """Validate that all required fields are present"""
    for field in required_fields:
        if field not in data or data[field] is None:
            raise ValidationError(f"Missing required field: {field}")
    return True

def validate_string_length(value: str, min_length: int = 1, max_length: int = 255) -> bool:
    """Validate string length"""
    if not isinstance(value, str):
        raise ValidationError("Value must be a string")
    if len(value) < min_length or len(value) > max_length:
        raise ValidationError(f"String length must be between {min_length} and {max_length}")
    return True

def validate_number_range(value: float, min_val: float, max_val: float) -> bool:
    """Validate number is within range"""
    if not isinstance(value, (int, float)):
        raise ValidationError("Value must be a number")
    if value < min_val or value > max_val:
        raise ValidationError(f"Value must be between {min_val} and {max_val}")
    return True

def validate_password_strength(password: str) -> bool:
    """Validate password strength"""
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters")
    if not any(c.isupper() for c in password):
        raise ValidationError("Password must contain uppercase letter")
    if not any(c.isdigit() for c in password):
        raise ValidationError("Password must contain a digit")
    return True
