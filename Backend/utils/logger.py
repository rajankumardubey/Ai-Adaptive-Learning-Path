import logging
import sys
from logging.handlers import RotatingFileHandler

def setup_logger(name: str, log_file: str = "app.log", level=logging.INFO):
    """Setup application logger"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # File handler
    file_handler = RotatingFileHandler(log_file, maxBytes=10485760, backupCount=5)
    file_handler.setLevel(level)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

# Create main logger
logger = setup_logger("adaptive_learning")
