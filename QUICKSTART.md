# Quick Start Guide

## Installation

1. Clone the repository:
```bash
git clone https://github.com/samir-djili/obfuscator.git
cd obfuscator
```

2. Install dependencies (optional):
```bash
pip install -r requirements.txt
```

## Basic Usage

### 1. Simple Obfuscation
```bash
python obfuscator.py --input my_script.py --output obfuscated_script.py
```

### 2. Choose Obfuscation Level
```bash
# Level 1: Basic obfuscation
python obfuscator.py --input script.py --output obfuscated.py --level 1

# Level 3: Advanced obfuscation
python obfuscator.py --input script.py --output obfuscated.py --level 3
```

### 3. Specific Techniques
```bash
# Use only string and numeric obfuscation
python obfuscator.py --input script.py --output obfuscated.py --techniques string_encoding,numeric_obfuscation
```

### 4. Preview Without Writing
```bash
python obfuscator.py --input script.py --output temp.py --dry-run
```

### 5. Verbose Output
```bash
python obfuscator.py --input script.py --output obfuscated.py --verbose
```

## Configuration File

Create `config.json`:
```json
{
  "default_level": 2,
  "custom_encodings": {
    "string_encoding": "base64",
    "name_pattern": "hex"
  },
  "excluded_patterns": ["__main__", "__init__"]
}
```

Use with:
```bash
python obfuscator.py --input script.py --output obfuscated.py --config config.json
```

## Examples

### Before Obfuscation
```python
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total

result = calculate_sum([1, 2, 3, 4, 5])
print(f"Sum: {result}")
```

### After Obfuscation (Level 2)
```python
def kL9mQp2x(R4nW8vYz):
    xT5bN1 = (1-1)
    for mF7gK in R4nW8vYz:
        xT5bN1 += mF7gK
    return xT5bN1

oP3sM = kL9mQp2x([(2-1), (4-2), (5-2), (6-2), (7-2)])
print(f"''.join([chr(char_code) for char_code in [83, 117, 109, 58, 32]]): {oP3sM}")
```

## Programmatic Usage

```python
from languages.python.obfuscator import PythonObfuscator

# Initialize obfuscator
obfuscator = PythonObfuscator(level=2)

# Obfuscate code
original_code = """
def hello_world():
    print("Hello, World!")
"""

obfuscated = obfuscator.obfuscate(original_code)
print(obfuscated)
```

## Testing Your Obfuscated Code

Always test that your obfuscated code works:

```bash
# Original
python my_script.py

# Obfuscated
python obfuscated_script.py
```

Both should produce the same output!

## Tips for Best Results

1. **Start with Level 1**: Test with basic obfuscation first
2. **Use Dry Run**: Preview results with `--dry-run`
3. **Check Syntax**: Ensure obfuscated code is valid Python
4. **Test Functionality**: Verify obfuscated code works correctly
5. **Backup Originals**: Always keep original source files

## Common Issues

**Issue**: Syntax errors in obfuscated code
**Solution**: Try lower obfuscation level or specific techniques

**Issue**: f-strings not working properly
**Solution**: Use Level 1 or avoid f-string intensive code for now

**Issue**: Import errors
**Solution**: Avoid dynamic import obfuscation for complex imports

## Need Help?

- Check the examples in `examples/` directory
- Run tests with `python -m pytest tests/`
- Review `PROJECT_STATUS.md` for current capabilities
- Use `--verbose` flag for debugging information

Happy obfuscating! 🔒
