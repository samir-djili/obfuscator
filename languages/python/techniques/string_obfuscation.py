"""
String obfuscation techniques for Python code.
"""

import re
import random
import base64
from typing import Dict, List, Any, Optional


class StringObfuscator:
    """
    Handles various string obfuscation techniques for Python code.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the string obfuscator.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.string_counter = 0
        self.string_mapping = {}
    
    def encode_strings(self, code: str, context: Dict[str, Any]) -> str:
        """
        Basic string encoding using character codes.
        
        Args:
            code: Source code
            context: Obfuscation context
            
        Returns:
            Code with encoded strings
        """
        def replace_string(match):
            full_match = match.group(0)
            quote = match.group(1)
            content = match.group(2)
            
            # Skip empty strings and very short strings
            if len(content) < 2:
                return full_match
            
            # Skip docstrings (triple quoted strings)
            if len(full_match) > 6 and (full_match.startswith('"""') or full_match.startswith("'''")):
                return full_match
            
            # Create character code representation
            char_codes = [str(ord(c)) for c in content]
            encoded = f"''.join([chr(char_code) for char_code in [{', '.join(char_codes)}]])"
            
            return encoded
        
        # Pattern to match ONLY simple string literals (not f-strings, not inside f-strings)
        # This pattern excludes f-strings and strings that are part of f-string expressions
        lines = code.split('\n')
        result_lines = []
        
        for line in lines:
            # Skip lines that contain f-strings to avoid breaking them
            if 'f"' in line or "f'" in line:
                result_lines.append(line)
            else:
                # Pattern for simple string literals only
                pattern = r'(?<!f)(["\'])([^"\'\\]*(?:\\.[^"\'\\]*)*)\1(?!\1)'
                processed_line = re.sub(pattern, replace_string, line)
                result_lines.append(processed_line)
        
        return '\n'.join(result_lines)
    
    def advanced_encoding(self, code: str, context: Dict[str, Any]) -> str:
        """
        Advanced string encoding with multiple methods.
        
        Args:
            code: Source code
            context: Obfuscation context
            
        Returns:
            Code with advanced string encoding
        """
        def replace_string(match):
            full_match = match.group(0)
            quote = match.group(1)
            content = match.group(2)
            
            if len(content) < 2:
                return full_match
            
            # Choose random encoding method
            methods = ['char_codes', 'base64', 'hex', 'split_concat']
            method = random.choice(methods)
            
            if method == 'char_codes':
                char_codes = [str(ord(c)) for c in content]
                return f"''.join([chr(char_code) for char_code in [{', '.join(char_codes)}]])"
            
            elif method == 'base64':
                encoded = base64.b64encode(content.encode()).decode()
                return f"__import__('base64').b64decode('{encoded}').decode()"
            
            elif method == 'hex':
                hex_str = content.encode().hex()
                return f"bytes.fromhex('{hex_str}').decode()"
            
            elif method == 'split_concat':
                # Split string and concatenate
                parts = self._split_string_random(content)
                quoted_parts = [f"'{part}'" for part in parts]
                return f"({'+'.join(quoted_parts)})"
            
            return full_match
        
        # Process line by line to avoid f-string issues
        lines = code.split('\n')
        result_lines = []
        
        for line in lines:
            # Skip lines that contain f-strings to avoid breaking them
            if 'f"' in line or "f'" in line:
                result_lines.append(line)
            else:
                pattern = r'(?<!f)(["\'])([^"\'\\]*(?:\\.[^"\'\\]*)*)\1(?!\1)'
                processed_line = re.sub(pattern, replace_string, line)
                result_lines.append(processed_line)
        
        return '\n'.join(result_lines)
    
    def dynamic_assembly(self, code: str, context: Dict[str, Any]) -> str:
        """
        Dynamic string assembly with function lookups.
        
        Args:
            code: Source code
            context: Obfuscation context
            
        Returns:
            Code with dynamic string assembly
        """
        string_functions = []
        
        def replace_string(match):
            full_match = match.group(0)
            quote = match.group(1)
            content = match.group(2)
            
            if len(content) < 3:
                return full_match
            
            # Create a function that returns this string
            func_name = f"_str_{self.string_counter}"
            self.string_counter += 1
            
            # Create function with obfuscated string assembly
            char_codes = [str(ord(c)) for c in content]
            func_code = f"""
def {func_name}():
    return ''.join([chr(c) for c in [{', '.join(char_codes)}]])
"""
            string_functions.append(func_code)
            
            return f"{func_name}()"
        
        # Replace strings with function calls
        pattern = r'(["\'])([^"\'\\]*(?:\\.[^"\'\\]*)*)\1'
        modified_code = re.sub(pattern, replace_string, code)
        
        # Add string functions at the beginning
        if string_functions:
            functions_code = '\n'.join(string_functions)
            return functions_code + '\n\n' + modified_code
        
        return modified_code
    
    def create_string_lookup_table(self, code: str, context: Dict[str, Any]) -> str:
        """
        Create a lookup table for all strings.
        
        Args:
            code: Source code
            context: Obfuscation context
            
        Returns:
            Code with string lookup table
        """
        strings_found = []
        
        def collect_string(match):
            content = match.group(2)
            if len(content) >= 2:
                strings_found.append(content)
            return match.group(0)
        
        # First pass: collect all strings
        pattern = r'(["\'])([^"\'\\]*(?:\\.[^"\'\\]*)*)\1'
        re.sub(pattern, collect_string, code)
        
        if not strings_found:
            return code
        
        # Create lookup table
        table_name = f"_strings_{random.randint(1000, 9999)}"
        lookup_code = f"{table_name} = {{\n"
        
        string_mapping = {}
        for i, string_val in enumerate(set(strings_found)):
            key = f"s{i}"
            encoded = base64.b64encode(string_val.encode()).decode()
            lookup_code += f"    '{key}': __import__('base64').b64decode('{encoded}').decode(),\n"
            string_mapping[string_val] = key
        
        lookup_code += "}\n\n"
        
        # Second pass: replace strings with lookups
        def replace_with_lookup(match):
            content = match.group(2)
            if content in string_mapping:
                return f"{table_name}['{string_mapping[content]}']"
            return match.group(0)
        
        modified_code = re.sub(pattern, replace_with_lookup, code)
        
        return lookup_code + modified_code
    
    def _split_string_random(self, text: str, min_parts: int = 2, max_parts: int = 4) -> List[str]:
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
        if num_parts <= 1:
            return [text]
        
        split_points = sorted(random.sample(range(1, len(text)), num_parts - 1))
        
        parts = []
        start = 0
        for point in split_points:
            parts.append(text[start:point])
            start = point
        parts.append(text[start:])
        
        return parts
    
    def obfuscate_format_strings(self, code: str, context: Dict[str, Any]) -> str:
        """
        Obfuscate f-strings and format strings.
        
        Args:
            code: Source code
            context: Obfuscation context
            
        Returns:
            Code with obfuscated format strings
        """
        # Simple f-string replacement (basic implementation)
        def replace_fstring(match):
            content = match.group(1)
            # Convert f"text {var}" to "text {}".format(var)
            # This is a simplified implementation
            return f'"{content}".format()'
        
        # Basic f-string pattern (simplified)
        fstring_pattern = r'f["\']([^"\']*)["\']'
        return re.sub(fstring_pattern, replace_fstring, code)
