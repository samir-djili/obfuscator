"""
Utility functions for the obfuscator.
"""

import random
import string
import hashlib
import base64
import re
from typing import List, Dict, Any, Optional, Union


def generate_random_identifier(length: int = 8, prefix: str = "_") -> str:
    """
    Generate a random identifier.
    
    Args:
        length: Length of the random part
        prefix: Prefix for the identifier
        
    Returns:
        Random identifier string
    """
    chars = string.ascii_letters + string.digits
    random_part = ''.join(random.choices(chars, k=length))
    return f"{prefix}{random_part}"


def generate_hex_identifier(length: int = 8, prefix: str = "_0x") -> str:
    """
    Generate a hex-style identifier.
    
    Args:
        length: Length of the hex part
        prefix: Prefix for the identifier
        
    Returns:
        Hex-style identifier string
    """
    hex_chars = '0123456789abcdef'
    hex_part = ''.join(random.choices(hex_chars, k=length))
    return f"{prefix}{hex_part}"


def hash_string(text: str, algorithm: str = 'md5') -> str:
    """
    Generate hash of a string.
    
    Args:
        text: Text to hash
        algorithm: Hash algorithm ('md5', 'sha1', 'sha256')
        
    Returns:
        Hex digest of the hash
    """
    if algorithm == 'md5':
        return hashlib.md5(text.encode()).hexdigest()
    elif algorithm == 'sha1':
        return hashlib.sha1(text.encode()).hexdigest()
    elif algorithm == 'sha256':
        return hashlib.sha256(text.encode()).hexdigest()
    else:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")


def encode_base64(text: str) -> str:
    """
    Encode text to base64.
    
    Args:
        text: Text to encode
        
    Returns:
        Base64 encoded string
    """
    return base64.b64encode(text.encode()).decode()


def decode_base64(encoded: str) -> str:
    """
    Decode base64 text.
    
    Args:
        encoded: Base64 encoded string
        
    Returns:
        Decoded text
    """
    return base64.b64decode(encoded).decode()


def string_to_char_codes(text: str) -> List[int]:
    """
    Convert string to list of character codes.
    
    Args:
        text: Input string
        
    Returns:
        List of character codes
    """
    return [ord(c) for c in text]


def char_codes_to_string(codes: List[int]) -> str:
    """
    Convert list of character codes to string.
    
    Args:
        codes: List of character codes
        
    Returns:
        Resulting string
    """
    return ''.join(chr(code) for code in codes)


def split_string_random(text: str, min_parts: int = 2, max_parts: int = 5) -> List[str]:
    """
    Split string into random parts.
    
    Args:
        text: String to split
        min_parts: Minimum number of parts
        max_parts: Maximum number of parts
        
    Returns:
        List of string parts
    """
    if len(text) <= 1:
        return [text]
    
    num_parts = random.randint(min_parts, min(max_parts, len(text)))
    split_points = sorted(random.sample(range(1, len(text)), num_parts - 1))
    
    parts = []
    start = 0
    for point in split_points:
        parts.append(text[start:point])
        start = point
    parts.append(text[start:])
    
    return parts


def find_string_literals(code: str, quote_chars: str = '"\'') -> List[Dict[str, Any]]:
    """
    Find string literals in code.
    
    Args:
        code: Source code
        quote_chars: Quote characters to look for
        
    Returns:
        List of dictionaries with string literal information
    """
    literals = []
    i = 0
    while i < len(code):
        if code[i] in quote_chars:
            quote = code[i]
            start = i
            i += 1
            
            # Find the end of the string
            while i < len(code):
                if code[i] == quote and (i == 0 or code[i-1] != '\\'):
                    end = i + 1
                    literal_text = code[start:end]
                    content = code[start+1:i]  # Without quotes
                    
                    literals.append({
                        'start': start,
                        'end': end,
                        'quote': quote,
                        'content': content,
                        'full_literal': literal_text
                    })
                    break
                elif code[i] == '\\' and i + 1 < len(code):
                    i += 2  # Skip escaped character
                else:
                    i += 1
        else:
            i += 1
    
    return literals


def find_identifiers(code: str, excluded_keywords: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """
    Find identifiers (variable/function names) in code.
    
    Args:
        code: Source code
        excluded_keywords: Keywords to exclude from results
        
    Returns:
        List of dictionaries with identifier information
    """
    if excluded_keywords is None:
        excluded_keywords = [
            'def', 'class', 'if', 'else', 'elif', 'for', 'while', 'try', 'except',
            'finally', 'with', 'import', 'from', 'as', 'return', 'yield', 'pass',
            'break', 'continue', 'and', 'or', 'not', 'in', 'is', 'True', 'False',
            'None', 'lambda', 'global', 'nonlocal', 'assert', 'del', 'raise'
        ]
    
    # Pattern for Python identifiers
    identifier_pattern = r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'
    
    identifiers = []
    for match in re.finditer(identifier_pattern, code):
        name = match.group()
        if name not in excluded_keywords:
            identifiers.append({
                'name': name,
                'start': match.start(),
                'end': match.end()
            })
    
    return identifiers


def shuffle_list(items: List[Any]) -> List[Any]:
    """
    Shuffle a list randomly.
    
    Args:
        items: List to shuffle
        
    Returns:
        Shuffled list
    """
    shuffled = items.copy()
    random.shuffle(shuffled)
    return shuffled


def create_dummy_functions(count: int = 5) -> List[str]:
    """
    Create dummy function definitions for dead code insertion.
    
    Args:
        count: Number of dummy functions to create
        
    Returns:
        List of dummy function code strings
    """
    dummy_functions = []
    
    for i in range(count):
        name = generate_random_identifier()
        params = random.randint(0, 3)
        param_names = [generate_random_identifier(length=4) for _ in range(params)]
        
        operations = [
            f"return {random.randint(1, 100)}",
            f"return sum([{', '.join(str(random.randint(1, 10)) for _ in range(3))}])",
            f"return len('{generate_random_identifier(length=10)}')",
            f"return {''.join(random.choices(string.digits, k=5))} * 2",
        ]
        
        func_body = random.choice(operations)
        
        if param_names:
            func_def = f"def {name}({', '.join(param_names)}):\n    {func_body}"
        else:
            func_def = f"def {name}():\n    {func_body}"
        
        dummy_functions.append(func_def)
    
    return dummy_functions


def obfuscate_numeric_literals(code: str) -> str:
    """
    Obfuscate numeric literals in code.
    
    Args:
        code: Source code
        
    Returns:
        Code with obfuscated numeric literals
    """
    def replace_number(match):
        num = int(match.group())
        if num == 0:
            return "(1-1)"
        elif num == 1:
            return "(2-1)"
        elif num > 1:
            # Create a simple arithmetic expression
            a = random.randint(1, num)
            b = num - a
            return f"({a}+{b})"
        else:  # negative numbers
            return f"(-{abs(num)})"
    
    # Pattern for integer literals (not in strings)
    number_pattern = r'\b\d+\b'
    
    return re.sub(number_pattern, replace_number, code)


def add_code_comments(code: str, comment_density: float = 0.1) -> str:
    """
    Add random comments to code for obfuscation.
    
    Args:
        code: Source code
        comment_density: Fraction of lines to add comments to
        
    Returns:
        Code with added comments
    """
    comments = [
        "# Optimization marker",
        "# Runtime checkpoint", 
        "# Memory allocation point",
        "# Performance critical section",
        "# Security validation",
        "# Data integrity check",
        "# Cache optimization",
        "# Thread synchronization point"
    ]
    
    lines = code.split('\n')
    result = []
    
    for line in lines:
        result.append(line)
        if random.random() < comment_density and line.strip():
            result.append(f"    {random.choice(comments)}")
    
    return '\n'.join(result)
