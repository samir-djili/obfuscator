"""
Final demonstration of the obfuscator capabilities.
"""

import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from languages.python.obfuscator import PythonObfuscator

def demonstrate_obfuscation():
    """Demonstrate the obfuscator with different levels."""
    
    # Sample code to obfuscate
    sample_code = '''
def calculate_fibonacci(n):
    """Calculate the nth Fibonacci number."""
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

def format_result(number, position):
    """Format the result for display."""
    return f"Fibonacci({position}) = {number}"

def main():
    """Main function to demonstrate Fibonacci calculation."""
    position = 10
    result = calculate_fibonacci(position)
    message = format_result(result, position)
    print(message)
    
    # Test with a list of values
    test_values = [0, 1, 5, 8, 10]
    for val in test_values:
        fib_val = calculate_fibonacci(val)
        print(f"F({val}) = {fib_val}")

if __name__ == "__main__":
    main()
'''
    
    print("="*60)
    print("OBFUSCATION DEMONSTRATION")
    print("="*60)
    
    print("\nOriginal Code:")
    print("-" * 40)
    print(sample_code)
    
    # Test different levels
    levels = [1, 2, 3]
    
    for level in levels:
        print(f"\n{'='*60}")
        print(f"LEVEL {level} OBFUSCATION")
        print(f"{'='*60}")
        
        obfuscator = PythonObfuscator(level=level)
        obfuscated = obfuscator.obfuscate(sample_code)
        
        print(f"Obfuscated Code (Level {level}):")
        print("-" * 40)
        print(obfuscated[:300] + "..." if len(obfuscated) > 300 else obfuscated)
        
        print(f"\nStats:")
        print(f"  Original size: {len(sample_code)} characters")
        print(f"  Obfuscated size: {len(obfuscated)} characters")
        print(f"  Size increase: {((len(obfuscated) - len(sample_code)) / len(sample_code) * 100):.1f}%")
        
        # Test if the obfuscated code still works
        try:
            exec_globals = {}
            exec(obfuscated, exec_globals)
            print("  ✓ Obfuscated code executes successfully")
        except Exception as e:
            print(f"  ✗ Obfuscated code failed: {e}")
    
    print(f"\n{'='*60}")
    print("TECHNIQUE-SPECIFIC DEMONSTRATIONS")
    print(f"{'='*60}")
    
    # Demonstrate specific techniques
    techniques_demo = [
        (['numeric_obfuscation'], "Numeric Obfuscation"),
        (['string_encoding'], "String Encoding"),
        (['basic_name_change'], "Name Obfuscation"),
    ]
    
    for techniques, description in techniques_demo:
        print(f"\n{description}:")
        print("-" * 40)
        
        obfuscator = PythonObfuscator(level=1)
        obfuscator.set_techniques(techniques)
        obfuscated = obfuscator.obfuscate(sample_code)
        
        print(obfuscated[:200] + "..." if len(obfuscated) > 200 else obfuscated)

if __name__ == "__main__":
    demonstrate_obfuscation()
