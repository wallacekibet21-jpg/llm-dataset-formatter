"""
Text cleaning utilities for data preprocessing.

This module provides functions to clean and normalize text data
from raw evaluation logs.
"""

import re
from typing import Any, Dict, Optional


def clean_text(text: str) -> str:
    """
    Clean and normalize text data.
    
    Args:
        text (str): Raw text to clean
        
    Returns:
        str: Cleaned text
    """
    if not isinstance(text, str):
        return str(text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    # Remove special control characters
    text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', text)
    
    # Normalize unicode
    text = text.encode('utf-8', 'ignore').decode('utf-8')
    
    return text


def sanitize_data(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitize all text fields in a record.
    
    Args:
        record (Dict): Data record to sanitize
        
    Returns:
        Dict: Sanitized record
    """
    sanitized = {}
    
    for key, value in record.items():
        if isinstance(value, str):
            sanitized[key] = clean_text(value)
        elif isinstance(value, dict):
            sanitized[key] = sanitize_data(value)
        elif isinstance(value, list):
            sanitized[key] = [
                clean_text(item) if isinstance(item, str) else item
                for item in value
            ]
        else:
            sanitized[key] = value
    
    return sanitized


def remove_duplicates(text: str) -> str:
    """
    Remove duplicate consecutive words.
    
    Args:
        text (str): Text to process
        
    Returns:
        str: Text with duplicates removed
    """
    words = text.split()
    deduped = []
    prev_word = None
    
    for word in words:
        if word.lower() != prev_word:
            deduped.append(word)
            prev_word = word.lower()
    
    return ' '.join(deduped)


def normalize_numbers(text: str) -> str:
    """
    Normalize number formatting.
    
    Args:
        text (str): Text containing numbers
        
    Returns:
        str: Text with normalized numbers
    """
    # Normalize spaces around numbers
    text = re.sub(r'\s*(\d+)\s*', r' \1 ', text)
    
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()
