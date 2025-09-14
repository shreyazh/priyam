"""
String utilities for common string operations.
"""

import re
import unicodedata

def title_case_with_exceptions(text, exceptions=None):
    """
    Convert text to title case with exceptions for specific words.
    
    Args:
        text (str): The text to convert to title case.
        exceptions (list): List of words to keep in lowercase.
        
    Returns:
        str: Text in title case with exceptions applied.
        
    Example:
        >>> title_case_with_exceptions("the lord of the rings", ["the", "of"])
        'The Lord of the Rings'
    """
    if exceptions is None:
        exceptions = ["a", "an", "the", "and", "but", "or", "for", "nor", 
                     "on", "at", "to", "from", "by", "of", "in"]
    
    words = text.split()
    result = []
    
    for i, word in enumerate(words):
        if i == 0 or i == len(words) - 1 or word.lower() not in exceptions:
            result.append(word.capitalize())
        else:
            result.append(word.lower())
    
    return " ".join(result)

def reverse_words(text):
    """
    Reverse the order of words in a string.
    
    Args:
        text (str): The text to reverse.
        
    Returns:
        str: Text with words reversed.
        
    Example:
        >>> reverse_words("Hello World")
        'World Hello'
    """
    words = text.split()
    return " ".join(reversed(words))

def slugify(text, separator="-"):
    """
    Convert text to a slug for use in URLs.
    
    Args:
        text (str): The text to convert to a slug.
        separator (str): The separator to use between words.
        
    Returns:
        str: A slugified version of the text.
        
    Example:
        >>> slugify("Hello World!")
        'hello-world'
    """
    # Normalize unicode characters
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    
    # Convert to lowercase and remove special characters
    text = re.sub(r"[^\w\s-]", "", text.lower())
    
    # Replace spaces and hyphens with the separator
    text = re.sub(r"[-\s]+", separator, text)
    
    # Remove leading/trailing separators
    return text.strip(separator)