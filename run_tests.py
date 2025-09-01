#!/usr/bin/env python3
"""
Simple test runner for the obfuscator project.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_tests():
    """Run basic functionality tests."""
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    print("🧪 Running Obfuscator Tests...")
    print("=" * 50)
    
    # Test 1: Import test
    print("\n1. Testing imports...")
    try:
        import obfuscator
        from languages.python.obfuscator import PythonObfuscator
        print("✅ All imports successful")
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False
    
    # Test 2: Basic obfuscation test
    print("\n2. Testing basic obfuscation...")
    try:
        result = subprocess.run([
            sys.executable, "obfuscator.py", 
            "-i", "tests/sample_files/simple.py",
            "-o", "tests/sample_files/test_runner_output.py",
            "--techniques", "variable_name_obfuscation"
        ], capture_output=True, text=True, cwd=project_root)
        
        if result.returncode == 0:
            print("✅ Basic obfuscation successful")
            
            # Test execution
            result2 = subprocess.run([
                sys.executable, "tests/sample_files/test_runner_output.py"
            ], capture_output=True, text=True, cwd=project_root)
            
            if result2.returncode == 0:
                print("✅ Obfuscated code executes correctly")
            else:
                print(f"❌ Obfuscated code execution failed: {result2.stderr}")
                return False
        else:
            print(f"❌ Obfuscation failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    # Test 3: Advanced obfuscation test
    print("\n3. Testing advanced obfuscation...")
    try:
        result = subprocess.run([
            sys.executable, "obfuscator.py", 
            "-i", "tests/sample_files/complex.py",
            "-o", "tests/sample_files/test_runner_complex.py",
            "--techniques", "dynamic_imports,function_name_obfuscation,variable_name_obfuscation,numeric_obfuscation"
        ], capture_output=True, text=True, cwd=project_root)
        
        if result.returncode == 0:
            print("✅ Advanced obfuscation successful")
        else:
            print(f"❌ Advanced obfuscation failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Advanced test failed: {e}")
        return False
    
    # Cleanup
    cleanup_files = [
        "tests/sample_files/test_runner_output.py",
        "tests/sample_files/test_runner_complex.py"
    ]
    
    for file in cleanup_files:
        try:
            if os.path.exists(file):
                os.remove(file)
        except:
            pass
    
    print("\n🎉 All tests passed!")
    print("=" * 50)
    return True

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
