"""
Basic usage example for the code obfuscator.
"""

# Example 1: Basic obfuscation
from obfuscator import CodeObfuscator

def example_basic_obfuscation():
    """Demonstrate basic obfuscation."""
    
    # Original code to obfuscate
    original_code = '''
def calculate_sum(numbers):
    """Calculate the sum of a list of numbers."""
    total = 0
    for num in numbers:
        total += num
    return total

def main():
    """Main function."""
    data = [1, 2, 3, 4, 5]
    result = calculate_sum(data)
    print(f"The sum is: {result}")

if __name__ == "__main__":
    main()
'''
    
    # Initialize obfuscator with level 2
    obfuscator = CodeObfuscator(language='python', level=2)
    
    # Obfuscate the code
    obfuscated_code = obfuscator.obfuscate(original_code)
    
    print("Original code:")
    print(original_code)
    print("\n" + "="*50 + "\n")
    print("Obfuscated code:")
    print(obfuscated_code)

def example_with_config():
    """Demonstrate obfuscation with custom configuration."""
    
    config = {
        'randomize_seeds': True,
        'custom_encodings': {
            'string_encoding': 'base64',
            'name_pattern': 'hex'
        },
        'excluded_patterns': ['__main__', '__init__']
    }
    
    code = '''
class Calculator:
    def __init__(self):
        self.history = []
    
    def add(self, a, b):
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def get_history(self):
        return self.history

calc = Calculator()
result = calc.add(10, 20)
print("Result:", result)
'''
    
    obfuscator = CodeObfuscator(language='python', level=3, config=config)
    obfuscated = obfuscator.obfuscate(code)
    
    print("Obfuscated with custom config:")
    print(obfuscated)

if __name__ == "__main__":
    print("Running basic obfuscation example...")
    example_basic_obfuscation()
    
    print("\n" + "="*70 + "\n")
    
    print("Running configuration example...")
    example_with_config()
