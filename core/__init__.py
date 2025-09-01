"""
Core module for the code obfuscator.
"""

from .base_obfuscator import BaseObfuscator
from .language_detector import LanguageDetector
from .technique_manager import TechniqueManager
from .utils import *

__all__ = [
    'BaseObfuscator',
    'LanguageDetector', 
    'TechniqueManager',
]
