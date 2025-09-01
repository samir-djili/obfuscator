"""
Advanced obfuscation techniques demonstration.
"""

from obfuscator import CodeObfuscator

def example_advanced_string_obfuscation():
    """Demonstrate advanced string obfuscation techniques."""
    
    code = '''
def greet_user(name):
    message = "Hello, " + name + "!"
    warning = "This is a security warning"
    success = "Operation completed successfully"
    return message

password = "secret123"
api_key = "api_key_12345"
database_url = "mongodb://localhost:27017/mydb"

print(greet_user("Alice"))
print(f"Using API key: {api_key}")
'''
    
    obfuscator = CodeObfuscator(
        language='python', 
        level=3,
        config={'verbose': True}
    )
    
    # Use specific string obfuscation techniques
    obfuscator.set_techniques(['advanced_string_obfuscation', 'dynamic_string_assembly'])
    
    obfuscated = obfuscator.obfuscate(code)
    
    print("Advanced String Obfuscation:")
    print(obfuscated)

def example_control_flow_obfuscation():
    """Demonstrate control flow obfuscation."""
    
    code = '''
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

def process_data(data):
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
        else:
            result.append(0)
    return result

numbers = [1, -2, 3, -4, 5]
processed = process_data(numbers)
fib_result = fibonacci(10)

print("Processed:", processed)
print("Fibonacci(10):", fib_result)
'''
    
    obfuscator = CodeObfuscator(language='python', level=3)
    obfuscator.set_techniques(['control_flow_flattening', 'simple_control_flow'])
    
    obfuscated = obfuscator.obfuscate(code)
    
    print("Control Flow Obfuscation:")
    print(obfuscated)

def example_name_obfuscation():
    """Demonstrate variable and function name obfuscation."""
    
    code = '''
class UserManager:
    def __init__(self):
        self.users = {}
        self.current_user = None
    
    def create_user(self, username, email):
        user_id = len(self.users) + 1
        user_data = {
            'id': user_id,
            'username': username,
            'email': email,
            'active': True
        }
        self.users[user_id] = user_data
        return user_id
    
    def get_user(self, user_id):
        return self.users.get(user_id)
    
    def authenticate_user(self, username):
        for user in self.users.values():
            if user['username'] == username:
                self.current_user = user
                return True
        return False

manager = UserManager()
user_id = manager.create_user("alice", "alice@example.com")
user_info = manager.get_user(user_id)
auth_result = manager.authenticate_user("alice")

print(f"Created user: {user_info}")
print(f"Authentication: {auth_result}")
'''
    
    obfuscator = CodeObfuscator(
        language='python', 
        level=2,
        config={
            'custom_encodings': {
                'name_pattern': 'hex'
            }
        }
    )
    
    obfuscator.set_techniques(['function_name_obfuscation', 'variable_name_obfuscation'])
    
    obfuscated = obfuscator.obfuscate(code)
    
    print("Name Obfuscation:")
    print(obfuscated)

def example_import_obfuscation():
    """Demonstrate import obfuscation."""
    
    code = '''
import os
import sys
import json
import base64
from datetime import datetime
from collections import defaultdict

def get_system_info():
    info = {
        'platform': sys.platform,
        'python_version': sys.version,
        'current_dir': os.getcwd(),
        'timestamp': datetime.now().isoformat()
    }
    return info

def encode_data(data):
    json_str = json.dumps(data)
    encoded = base64.b64encode(json_str.encode()).decode()
    return encoded

data_store = defaultdict(list)
system_info = get_system_info()
encoded_info = encode_data(system_info)

data_store['system'].append(encoded_info)
print("System info encoded and stored")
'''
    
    obfuscator = CodeObfuscator(language='python', level=3)
    obfuscator.set_techniques(['dynamic_imports'])
    
    obfuscated = obfuscator.obfuscate(code)
    
    print("Import Obfuscation:")
    print(obfuscated)

def example_maximum_obfuscation():
    """Demonstrate maximum obfuscation level."""
    
    code = '''
def calculate_score(values, weights):
    """Calculate weighted score."""
    if len(values) != len(weights):
        raise ValueError("Length mismatch")
    
    total_score = 0
    total_weight = 0
    
    for value, weight in zip(values, weights):
        total_score += value * weight
        total_weight += weight
    
    if total_weight == 0:
        return 0
    
    return total_score / total_weight

# Test data
test_values = [85, 90, 78, 92, 88]
test_weights = [0.2, 0.25, 0.15, 0.25, 0.15]

final_score = calculate_score(test_values, test_weights)
print(f"Final weighted score: {final_score:.2f}")

# Validation
if final_score > 85:
    print("Excellent performance!")
elif final_score > 75:
    print("Good performance!")
else:
    print("Needs improvement")
'''
    
    # Maximum obfuscation with all techniques
    obfuscator = CodeObfuscator(
        language='python', 
        level=4,
        config={
            'randomize_seeds': True,
            'verbose': False
        }
    )
    
    obfuscated = obfuscator.obfuscate(code)
    
    print("Maximum Obfuscation (Level 4):")
    print(obfuscated)

if __name__ == "__main__":
    examples = [
        ("Advanced String Obfuscation", example_advanced_string_obfuscation),
        ("Control Flow Obfuscation", example_control_flow_obfuscation),
        ("Name Obfuscation", example_name_obfuscation),
        ("Import Obfuscation", example_import_obfuscation),
        ("Maximum Obfuscation", example_maximum_obfuscation),
    ]
    
    for title, example_func in examples:
        print(f"\n{'='*60}")
        print(f"EXAMPLE: {title}")
        print('='*60)
        try:
            example_func()
        except Exception as e:
            print(f"Error running example: {e}")
        print("\n")
