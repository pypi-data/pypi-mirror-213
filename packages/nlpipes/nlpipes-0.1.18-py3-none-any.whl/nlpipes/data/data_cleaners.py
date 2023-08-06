"""Text-related util functions."""
from ftfy import fix_text
import re

def clean(text: str, lowercase: bool = False) -> str:
    """Clean text. Does the following:
        1. Replace whitespace characters with space
        2. Fix corrupted text encodings
        3. Lowercase (if specified)
        4. Remove non latin character
    """
    # Replace whitespace characters with spaces
    text = " ".join(text.split())

    # Fix encoded texts
    text = fix_text(text)

    # Lowercase text if specified
    if lowercase:
        text = text.lower()
        
    # Remove non latin character
    text = re.sub(r'[^\x00-\x7f]',r'', text)

    return text