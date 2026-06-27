from typing import Any, Dict

def safe_get(dictionary: Dict, *keys: str, default: Any = None) -> Any:
    """Safely get nested dictionary values"""
    for key in keys:
        if isinstance(dictionary, dict) and key in dictionary:
            dictionary = dictionary[key]
        else:
            return default
    return dictionary

def validate_email(email: str) -> bool:
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def paginate(items: list, page: int, page_size: int = 10) -> dict:
    """Paginate a list of items"""
    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size
    
    return {
        "items": items[start:end],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size
    }

def calculate_percentage(part: float, total: float) -> float:
    """Calculate percentage"""
    if total == 0:
        return 0.0
    return (part / total) * 100
