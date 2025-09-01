"""
Python obfuscation techniques.
"""

from .string_obfuscation import StringObfuscator
from .name_obfuscation import NameObfuscator
from .control_flow import ControlFlowObfuscator
from .dynamic_imports import DynamicImportObfuscator
from .bytecode_manipulation import BytecodeObfuscator

__all__ = [
    'StringObfuscator',
    'NameObfuscator',
    'ControlFlowObfuscator', 
    'DynamicImportObfuscator',
    'BytecodeObfuscator'
]
