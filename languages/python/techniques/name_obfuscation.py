"""
Name obfuscation techniques for Python code.
"""

import re
import ast
import random
import string
from typing import Dict, List, Any, Optional, Set


class NameObfuscator:
    """
    Handles variable and function name obfuscation for Python code.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the name obfuscator.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.name_mapping = {}
        self.reserved_names = self._get_reserved_names()
        self.counter = 0
    
    def _get_reserved_names(self) -> Set[str]:
        """Get Python reserved names that should not be obfuscated."""
        return {
            # Python keywords
            'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del',
            'elif', 'else', 'except', 'exec', 'finally', 'for', 'from', 'global',
            'if', 'import', 'in', 'is', 'lambda', 'not', 'or', 'pass', 'print',
            'raise', 'return', 'try', 'while', 'with', 'yield', 'True', 'False',
            'None', 'async', 'await', 'nonlocal',
            
            # Built-in functions
            'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray', 'bytes',
            'callable', 'chr', 'classmethod', 'compile', 'complex', 'delattr',
            'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'filter',
            'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr',
            'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance',
            'issubclass', 'iter', 'len', 'list', 'locals', 'map', 'max',
            'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord',
            'pow', 'property', 'range', 'repr', 'reversed', 'round', 'set',
            'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super',
            'tuple', 'type', 'vars', 'zip',
            
            # Common built-in methods and attributes
            'items', 'keys', 'values', 'get', 'pop', 'append', 'extend', 'insert',
            'remove', 'clear', 'copy', 'update', 'index', 'count', 'sort', 'reverse',
            'join', 'split', 'strip', 'replace', 'upper', 'lower', 'startswith',
            'endswith', 'find', 'rfind', 'isdigit', 'isalpha', 'isalnum', 'isspace',
            'format', 'encode', 'decode', 'read', 'write', 'close', 'open', 'seek',
            'tell', 'flush', 'readline', 'readlines', 'writelines',
            
            # Special methods and attributes
            '__init__', '__main__', '__name__', '__file__', '__doc__',
            '__dict__', '__class__', '__module__', '__bases__',
        }
    
    def basic_rename(self, code: str, context: Dict[str, Any]) -> str:
        """
        Basic variable and function name obfuscation.
        
        Args:
            code: Source code
            context: Obfuscation context
            
        Returns:
            Code with obfuscated names
        """
        try:
            tree = ast.parse(code)
            
            # Collect all identifiers
            identifiers = self._collect_identifiers(tree)
            
            # Create mapping for identifiers
            for identifier in identifiers:
                if identifier not in self.reserved_names:
                    if identifier not in self.name_mapping:
                        self.name_mapping[identifier] = self._generate_name()
            
            # Replace identifiers in code
            modified_code = self._replace_identifiers(code, self.name_mapping)
            
            # Update context
            context['variable_mapping'].update(self.name_mapping)
            
            return modified_code
            
        except SyntaxError:
            # Fallback to regex-based approach if AST parsing fails
            return self._regex_based_rename(code)
    
    def obfuscate_functions(self, code: str, context: Dict[str, Any]) -> str:
        """
        Obfuscate function names specifically.
        
        Args:
            code: Source code
            context: Obfuscation context
            
        Returns:
            Code with obfuscated function names
        """
        try:
            tree = ast.parse(code)
            function_names = self._collect_function_names(tree)
            
            # Add context reserved names to our reserved names
            all_reserved = self.reserved_names.copy()
            if 'reserved_names' in context:
                all_reserved.update(context['reserved_names'])
            
            function_mapping = {}
            for func_name in function_names:
                if func_name not in all_reserved:
                    function_mapping[func_name] = self._generate_name()
            
            modified_code = self._replace_identifiers(code, function_mapping)
            context['function_mapping'].update(function_mapping)
            
            return modified_code
            
        except SyntaxError:
            return code
    
    def obfuscate_variables(self, code: str, context: Dict[str, Any]) -> str:
        """
        Obfuscate variable names specifically.
        
        Args:
            code: Source code
            context: Obfuscation context
            
        Returns:
            Code with obfuscated variable names
        """
        try:
            tree = ast.parse(code)
            variable_names = self._collect_variable_names(tree)
            
            # Add context reserved names to our reserved names
            all_reserved = self.reserved_names.copy()
            if 'reserved_names' in context:
                all_reserved.update(context['reserved_names'])
            
            variable_mapping = {}
            for var_name in variable_names:
                if var_name not in all_reserved:
                    variable_mapping[var_name] = self._generate_name()
            
            modified_code = self._replace_identifiers(code, variable_mapping)
            context['variable_mapping'].update(variable_mapping)
            
            return modified_code
            
        except SyntaxError:
            return code
    
    def indirect_calls(self, code: str, context: Dict[str, Any]) -> str:
        """
        Create indirect function calls through proxy functions.
        
        Args:
            code: Source code
            context: Obfuscation context
            
        Returns:
            Code with indirect function calls
        """
        try:
            tree = ast.parse(code)
            function_calls = self._collect_function_calls(tree)
            
            # Create proxy functions
            proxy_code = []
            call_mapping = {}
            
            for func_name in function_calls:
                if func_name not in self.reserved_names:
                    proxy_name = self._generate_name()
                    call_mapping[func_name] = proxy_name
                    
                    # Create proxy function
                    proxy_func = f"""
def {proxy_name}(*args, **kwargs):
    return globals()['{func_name}'](*args, **kwargs)
"""
                    proxy_code.append(proxy_func)
            
            # Replace function calls
            modified_code = code
            for original, proxy in call_mapping.items():
                # Simple replacement - could be more sophisticated
                pattern = rf'\b{re.escape(original)}\s*\('
                replacement = f'{proxy}('
                modified_code = re.sub(pattern, replacement, modified_code)
            
            if proxy_code:
                return '\n'.join(proxy_code) + '\n\n' + modified_code
            
            return modified_code
            
        except SyntaxError:
            return code
    
    def dynamic_name_resolution(self, code: str, context: Dict[str, Any]) -> str:
        """
        Implement dynamic name resolution using getattr/globals.
        
        Args:
            code: Source code
            context: Obfuscation context
            
        Returns:
            Code with dynamic name resolution
        """
        # Create name resolver functions
        resolver_name = self._generate_name()
        resolver_code = f"""
def {resolver_name}(name):
    return globals().get(name) or getattr(__builtins__, name, None)

"""
        
        # This is a simplified implementation
        # In practice, you'd want more sophisticated analysis
        return resolver_code + code
    
    def _collect_identifiers(self, tree: ast.AST) -> Set[str]:
        """Collect all identifiers from AST."""
        identifiers = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                identifiers.add(node.id)
            elif isinstance(node, ast.FunctionDef):
                identifiers.add(node.name)
            elif isinstance(node, ast.ClassDef):
                identifiers.add(node.name)
        
        return identifiers
    
    def _collect_function_names(self, tree: ast.AST) -> Set[str]:
        """Collect function names from AST."""
        function_names = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                function_names.add(node.name)
        
        return function_names
    
    def _collect_variable_names(self, tree: ast.AST) -> Set[str]:
        """Collect variable names from AST."""
        variable_names = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                variable_names.add(node.id)
        
        return variable_names
    
    def _collect_function_calls(self, tree: ast.AST) -> Set[str]:
        """Collect function call names from AST."""
        function_calls = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    function_calls.add(node.func.id)
        
        return function_calls
    
    def _replace_identifiers(self, code: str, mapping: Dict[str, str]) -> str:
        """Replace identifiers in code using mapping, preserving f-strings and string literals."""
        modified_code = code
        
        # Sort by length (longest first) to avoid partial replacements
        sorted_names = sorted(mapping.keys(), key=len, reverse=True)
        
        for original_name, new_name in [(name, mapping[name]) for name in sorted_names]:
            # Skip single-letter replacements that could break f-strings
            if len(original_name) == 1 and original_name.lower() in ['f', 'r', 'b', 'u']:
                continue
            
            # More sophisticated replacement that avoids string literals
            modified_code = self._safe_replace_identifier(modified_code, original_name, new_name)
        
        return modified_code
    
    def _safe_replace_identifier(self, code: str, original_name: str, new_name: str) -> str:
        """Safely replace identifier avoiding string contexts."""
        import re
        
        # Simple approach: use basic patterns to avoid string literals
        parts = []
        current_pos = 0
        
        # Patterns for different string types
        patterns = [
            r'[fFrRbBuU]*""".*?"""',      # Triple double quoted
            r"[fFrRbBuU]*'''.*?'''",      # Triple single quoted  
            r'[fFrRbBuU]*"(?:[^"\\]|\\.)*"',  # Double quoted
            r"[fFrRbBuU]*'(?:[^'\\]|\\.)*'",  # Single quoted
            r'#[^\n]*'                    # Comments
        ]
        
        combined_pattern = '|'.join(f'({pattern})' for pattern in patterns)
        
        for match in re.finditer(combined_pattern, code, re.DOTALL):
            # Process code before the string
            before_string = code[current_pos:match.start()]
            if before_string:
                # Safe to replace identifiers here
                pattern = rf'\b{re.escape(original_name)}\b'
                before_string = re.sub(pattern, new_name, before_string)
                parts.append(before_string)
            
            # Handle the string itself
            string_content = match.group(0)
            if string_content.startswith(('f"', "f'", 'F"', "F'")):
                # This is an f-string, handle variable replacements inside {}
                parts.append(self._handle_fstring(string_content, original_name, new_name))
            else:
                # Regular string or comment, don't modify
                parts.append(string_content)
            
            current_pos = match.end()
        
        # Process remaining code after the last string
        if current_pos < len(code):
            remaining = code[current_pos:]
            pattern = rf'\b{re.escape(original_name)}\b'
            remaining = re.sub(pattern, new_name, remaining)
            parts.append(remaining)
        
        return ''.join(parts)
    
    def _handle_fstring(self, fstring_token: str, original_name: str, new_name: str) -> str:
        """Handle f-string replacements inside {} expressions."""
        import re
        
        # Find all {...} expressions in the f-string
        def replace_in_expression(match):
            expr = match.group(1)
            # Replace identifiers in the expression
            pattern = rf'\b{re.escape(original_name)}\b'
            modified_expr = re.sub(pattern, new_name, expr)
            return '{' + modified_expr + '}'
        
        # Replace expressions inside {}, preserving format specifiers
        result = re.sub(r'\{([^}:]+)(?::[^}]*)?\}', replace_in_expression, fstring_token)
        return result
    
    def _regex_based_rename(self, code: str) -> str:
        """Fallback regex-based renaming when AST parsing fails."""
        # Simple regex to find potential identifiers
        identifier_pattern = r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'
        
        identifiers = set(re.findall(identifier_pattern, code))
        identifiers -= self.reserved_names
        
        mapping = {}
        for identifier in identifiers:
            if identifier not in mapping:
                mapping[identifier] = self._generate_name()
        
        return self._replace_identifiers(code, mapping)
    
    def _generate_name(self) -> str:
        """Generate a new obfuscated name."""
        name_styles = self.config.get('custom_encodings', {}).get('name_pattern', 'random')
        
        if name_styles == 'hex':
            self.counter += 1
            return f"_0x{self.counter:04x}"
        elif name_styles == 'numeric':
            self.counter += 1
            return f"_var{self.counter}"
        else:  # random
            length = random.randint(6, 12)
            chars = string.ascii_letters + string.digits
            name = ''.join(random.choices(chars, k=length))
            # Ensure it starts with a letter or underscore
            if name[0].isdigit():
                name = '_' + name
            return name
