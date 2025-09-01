# Code Obfuscator

A powerful, modular code obfuscation tool that supports multiple programming languages with various levels of obfuscation techniques.

## Features

### Current Support
- **Python**: Multiple obfuscation levels and techniques
- **Modular Architecture**: Easy to extend for other languages

### Obfuscation Techniques

#### Level 1 - Basic Obfuscation
- Variable and function name randomization
- String literal replacement with character lookups
- Basic code structure modification

#### Level 2 - Intermediate Obfuscation
- Dynamic function name resolution
- String concatenation with randomized character arrays
- Control flow obfuscation
- Import statement obfuscation

#### Level 3 - Advanced Obfuscation
- Dynamic library loading
- Indirect function calls through proxy functions
- Complex string encoding (base64, hex, custom encoding)
- Code injection and self-modifying code patterns
- Dead code insertion

#### Level 4 - Expert Obfuscation
- Bytecode manipulation
- Runtime code generation
- Multiple encoding layers
- Anti-debugging techniques
- Code fragmentation and reassembly

## Installation

```bash
git clone https://github.com/samir-djili/obfuscator.git
cd obfuscator
pip install -r requirements.txt
```

## Quick Start

### Test the Installation
```bash
# Run the test suite to verify everything works
python run_tests.py
```

## Usage

### Command Line Interface

```bash
# Basic usage
python obfuscator.py --input file.py --output obfuscated_file.py

# Specify obfuscation level (1-4)
python obfuscator.py --input file.py --output obfuscated_file.py --level 3

# Specify language (auto-detected by default)
python obfuscator.py --input file.js --output obfuscated_file.js --language javascript

# Enable specific techniques
python obfuscator.py --input file.py --output obfuscated_file.py --techniques string_encoding,control_flow,dynamic_imports

# Randomize obfuscation patterns
python obfuscator.py --input file.py --output obfuscated_file.py --randomize

# Verbose output
python obfuscator.py --input file.py --output obfuscated_file.py --verbose
```

### Programmatic Usage

```python
from obfuscator import CodeObfuscator

# Initialize obfuscator
obfuscator = CodeObfuscator(language='python', level=3)

# Obfuscate code
with open('input.py', 'r') as f:
    original_code = f.read()

obfuscated_code = obfuscator.obfuscate(original_code)

# Save obfuscated code
with open('output.py', 'w') as f:
    f.write(obfuscated_code)
```

## Project Structure

```
obfuscator/
├── obfuscator.py              # Main CLI entry point
├── core/
│   ├── __init__.py
│   ├── base_obfuscator.py     # Base obfuscator class
│   ├── language_detector.py   # Auto-detect programming language
│   ├── technique_manager.py   # Manage obfuscation techniques
│   └── utils.py              # Utility functions
├── languages/
│   ├── __init__.py
│   ├── python/
│   │   ├── __init__.py
│   │   ├── obfuscator.py     # Python-specific obfuscator
│   │   └── techniques/
│   │       ├── __init__.py
│   │       ├── string_obfuscation.py
│   │       ├── name_obfuscation.py
│   │       ├── control_flow.py
│   │       ├── dynamic_imports.py
│   │       └── bytecode_manipulation.py
│   ├── javascript/            # Future: JavaScript support
│   │   └── ...
│   └── java/                 # Future: Java support
│       └── ...
├── tests/
│   ├── __init__.py
│   ├── test_python_obfuscator.py
│   └── sample_files/
│       ├── simple.py
│       ├── complex.py
│       └── ...
├── examples/
│   ├── basic_usage.py
│   ├── advanced_techniques.py
│   └── custom_obfuscator.py
├── requirements.txt
└── setup.py
```

## Supported Languages

| Language   | Status      | Obfuscation Levels | Techniques Available |
|------------|-------------|-------------------|---------------------|
| Python     | ✅ Active   | 1-4               | All                 |
| JavaScript | 🚧 Planned | TBD               | TBD                 |
| Java       | 🚧 Planned | TBD               | TBD                 |
| C++        | 🚧 Planned | TBD               | TBD                 |

## Obfuscation Techniques Detail

### String Obfuscation
- Character-by-character lookup functions
- Base64/Hex encoding with custom decoders
- String splitting and concatenation
- Dynamic string assembly

### Name Obfuscation
- Variable and function name randomization
- Namespace pollution
- Indirect name resolution

### Control Flow Obfuscation
- Opaque predicates
- Control flow flattening
- Bogus control flow insertion
- Loop unrolling and restructuring

### Dynamic Resolution
- Dynamic function name resolution
- Runtime import manipulation
- Indirect library loading
- Proxy function calls

## Configuration

Create a `config.json` file to customize obfuscation behavior:

```json
{
  "default_level": 2,
  "preserve_functionality": true,
  "randomize_seeds": true,
  "custom_encodings": {
    "string_encoding": "base64",
    "name_pattern": "random"
  },
  "excluded_patterns": [
    "__main__",
    "__init__",
    "if __name__"
  ]
}
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
print(f"The sum is: {result}")
```

### After Obfuscation (Level 3)
```python
def _0x4f2a():
    return ''.join([chr(99), chr(97), chr(108), chr(99), chr(117), chr(108), chr(97), chr(116), chr(101), chr(95), chr(115), chr(117), chr(109)])

def _0x8b1c():
    return [chr(110), chr(117), chr(109), chr(98), chr(101), chr(114), chr(115)]

_0x9d4e = globals()
_0x3a7f = getattr(_0x9d4e, 'get')(''.join(_0x4f2a().split('_')[0:2] + ['_'] + _0x4f2a().split('_')[2:]))

def _0x2c8a(_0x1b5d):
    _0x6e9f = 0
    for _0x4a3b in _0x1b5d:
        _0x6e9f += _0x4a3b
    return _0x6e9f

globals()[_0x4f2a()] = _0x2c8a
# ... continues with obfuscated logic
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-language`)
3. Implement your obfuscation techniques
4. Add comprehensive tests
5. Submit a pull request

### Adding New Languages

1. Create a new directory under `languages/`
2. Implement the language-specific obfuscator inheriting from `BaseObfuscator`
3. Create technique modules for the language
4. Add tests and examples
5. Update documentation

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is for educational and legitimate security testing purposes only. Users are responsible for ensuring compliance with applicable laws and regulations. The authors are not responsible for any misuse of this software.

## Roadmap

- [ ] JavaScript obfuscation support
- [ ] Java obfuscation support
- [ ] C++ obfuscation support
- [ ] Web-based interface
- [ ] Advanced anti-debugging techniques
- [ ] Custom encoding algorithms
- [ ] Performance optimization
- [ ] Integration with CI/CD pipelines