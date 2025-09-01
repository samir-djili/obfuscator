"""
Tests for the Python obfuscator.
"""

import pytest
import ast
from languages.python.obfuscator import PythonObfuscator
from languages.python.techniques.string_obfuscation import StringObfuscator
from languages.python.techniques.name_obfuscation import NameObfuscator


class TestPythonObfuscator:
    """Test cases for Python obfuscator."""
    
    def setup_method(self):
        """Setup for each test method."""
        self.obfuscator = PythonObfuscator(level=2)
    
    def test_basic_obfuscation(self):
        """Test basic obfuscation functionality."""
        code = '''
def hello():
    print("Hello, World!")

hello()
'''
        obfuscated = self.obfuscator.obfuscate(code)
        
        # Verify the obfuscated code is valid Python
        try:
            ast.parse(obfuscated)
        except SyntaxError:
            pytest.fail("Obfuscated code has invalid syntax")
        
        # Verify obfuscation occurred
        assert obfuscated != code
        assert len(obfuscated) > 0
    
    def test_string_literals_obfuscated(self):
        """Test that string literals are obfuscated."""
        code = '''
message = "Hello, World!"
print(message)
'''
        obfuscated = self.obfuscator.obfuscate(code)
        
        # Original string should not appear in obfuscated code
        assert '"Hello, World!"' not in obfuscated
        # But some form of the string reconstruction should be present
        assert 'Hello, World!' in obfuscated or 'chr(' in obfuscated
    
    def test_function_names_obfuscated(self):
        """Test that function names are obfuscated."""
        code = '''
def calculate_sum(numbers):
    return sum(numbers)

result = calculate_sum([1, 2, 3])
'''
        self.obfuscator.set_techniques(['function_name_obfuscation'])
        obfuscated = self.obfuscator.obfuscate(code)
        
        # Original function name should not appear (except in comments)
        lines_without_comments = [line for line in obfuscated.split('\n') 
                                 if not line.strip().startswith('#')]
        code_without_comments = '\n'.join(lines_without_comments)
        
        # Function name should be replaced in function definition and calls
        assert 'def calculate_sum(' not in code_without_comments
    
    def test_variable_names_obfuscated(self):
        """Test that variable names are obfuscated."""
        code = '''
user_name = "Alice"
user_age = 25
print(f"{user_name} is {user_age} years old")
'''
        self.obfuscator.set_techniques(['variable_name_obfuscation'])
        obfuscated = self.obfuscator.obfuscate(code)
        
        # Variable names should be replaced
        assert 'user_name' not in obfuscated or obfuscated.count('user_name') < code.count('user_name')
    
    def test_import_obfuscation(self):
        """Test import statement obfuscation."""
        code = '''
import os
import sys
from datetime import datetime

current_dir = os.getcwd()
platform = sys.platform
now = datetime.now()
'''
        self.obfuscator.set_techniques(['dynamic_imports'])
        obfuscated = self.obfuscator.obfuscate(code)
        
        # Direct import statements should be replaced
        assert 'import os' not in obfuscated
        assert 'import sys' not in obfuscated
        assert 'from datetime import datetime' not in obfuscated
    
    def test_different_obfuscation_levels(self):
        """Test different obfuscation levels produce different results."""
        code = '''
def test_function():
    message = "Test message"
    numbers = [1, 2, 3, 4, 5]
    return len(message) + sum(numbers)

result = test_function()
print(f"Result: {result}")
'''
        
        level1_obfuscator = PythonObfuscator(level=1)
        level2_obfuscator = PythonObfuscator(level=2)
        level3_obfuscator = PythonObfuscator(level=3)
        
        level1_result = level1_obfuscator.obfuscate(code)
        level2_result = level2_obfuscator.obfuscate(code)
        level3_result = level3_obfuscator.obfuscate(code)
        
        # All should be valid Python
        for result in [level1_result, level2_result, level3_result]:
            try:
                ast.parse(result)
            except SyntaxError:
                pytest.fail("Obfuscated code has invalid syntax")
        
        # Higher levels should generally produce more obfuscated code
        assert len(level3_result) >= len(level2_result)
        
        # Results should be different
        assert level1_result != level2_result
        assert level2_result != level3_result
    
    def test_preserve_functionality(self):
        """Test that obfuscated code preserves original functionality."""
        code = '''
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

result = factorial(5)
'''
        
        obfuscated = self.obfuscator.obfuscate(code)
        
        # Execute both codes and compare results
        original_globals = {}
        obfuscated_globals = {}
        
        exec(code, original_globals)
        exec(obfuscated, obfuscated_globals)
        
        assert original_globals['result'] == obfuscated_globals['result']
    
    def test_configuration_options(self):
        """Test configuration options affect obfuscation."""
        code = '''
test_variable = "test string"
'''
        
        # Test with hex naming pattern
        config_hex = {
            'custom_encodings': {
                'name_pattern': 'hex'
            }
        }
        obfuscator_hex = PythonObfuscator(level=2, config=config_hex)
        result_hex = obfuscator_hex.obfuscate(code)
        
        # Should contain hex-style identifiers
        assert '_0x' in result_hex or result_hex != code
        
        # Test with excluded patterns
        config_exclude = {
            'excluded_patterns': ['test_variable']
        }
        obfuscator_exclude = PythonObfuscator(level=2, config=config_exclude)
        result_exclude = obfuscator_exclude.obfuscate(code)
        
        # test_variable should be preserved
        assert 'test_variable' in result_exclude


class TestStringObfuscator:
    """Test cases for string obfuscation techniques."""
    
    def setup_method(self):
        """Setup for each test method."""
        self.string_obfuscator = StringObfuscator()
    
    def test_basic_string_encoding(self):
        """Test basic string encoding."""
        code = '''
message = "Hello World"
print(message)
'''
        
        result = self.string_obfuscator.encode_strings(code, {})
        
        # Original string literal should not be present
        assert '"Hello World"' not in result
        # Should contain character code representation
        assert 'chr(' in result
    
    def test_advanced_string_encoding(self):
        """Test advanced string encoding methods."""
        code = '''
text = "Advanced encoding test"
'''
        
        result = self.string_obfuscator.advanced_encoding(code, {})
        
        # Original string should not be present
        assert '"Advanced encoding test"' not in result
        # Should contain some form of encoding
        assert any(method in result for method in ['chr(', 'base64', 'hex', '+'])
    
    def test_dynamic_string_assembly(self):
        """Test dynamic string assembly."""
        code = '''
greeting = "Hello"
farewell = "Goodbye"
'''
        
        result = self.string_obfuscator.dynamic_assembly(code, {})
        
        # Should create functions for string assembly
        assert 'def _str_' in result
        # Original strings should not be present
        assert '"Hello"' not in result
        assert '"Goodbye"' not in result


class TestNameObfuscator:
    """Test cases for name obfuscation techniques."""
    
    def setup_method(self):
        """Setup for each test method."""
        self.name_obfuscator = NameObfuscator()
    
    def test_basic_rename(self):
        """Test basic variable and function renaming."""
        code = '''
def my_function(param1, param2):
    local_var = param1 + param2
    return local_var

result = my_function(1, 2)
'''
        
        result = self.name_obfuscator.basic_rename(code, {})
        
        # Function name should be obfuscated
        assert 'my_function' not in result or result.count('my_function') < code.count('my_function')
    
    def test_function_obfuscation(self):
        """Test specific function name obfuscation."""
        code = '''
def calculate():
    return 42

def process():
    return calculate()
'''
        
        result = self.name_obfuscator.obfuscate_functions(code, {})
        
        # Function names should be obfuscated
        assert 'def calculate(' not in result
        assert 'def process(' not in result
    
    def test_variable_obfuscation(self):
        """Test specific variable name obfuscation."""
        code = '''
user_name = "Alice"
user_age = 25
user_data = {"name": user_name, "age": user_age}
'''
        
        result = self.name_obfuscator.obfuscate_variables(code, {})
        
        # Variable names should be obfuscated
        original_count = code.count('user_name') + code.count('user_age') + code.count('user_data')
        result_count = result.count('user_name') + result.count('user_age') + result.count('user_data')
        
        assert result_count < original_count
    
    def test_reserved_names_preservation(self):
        """Test that reserved names are not obfuscated."""
        code = '''
def main():
    print("Hello")
    return True

if __name__ == "__main__":
    main()
'''
        
        result = self.name_obfuscator.basic_rename(code, {})
        
        # Reserved names should be preserved
        assert '__name__' in result
        assert '__main__' in result
        assert 'print' in result


if __name__ == "__main__":
    pytest.main([__file__])
