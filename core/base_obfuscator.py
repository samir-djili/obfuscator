"""
Base obfuscator class that all language-specific obfuscators inherit from.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import random
import string


class BaseObfuscator(ABC):
    """
    Abstract base class for all language-specific obfuscators.
    """
    
    def __init__(self, level: int = 2, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the base obfuscator.
        
        Args:
            level: Obfuscation level (1-4)
            config: Configuration dictionary
        """
        self.level = level
        self.config = config or {}
        self.techniques = []
        self.random_seed = self.config.get('randomize_seeds', True)
        
        if self.random_seed:
            random.seed()
        
        # Initialize technique mapping
        self._init_techniques()
    
    @abstractmethod
    def _init_techniques(self):
        """Initialize available techniques for this language."""
        pass
    
    @abstractmethod
    def obfuscate(self, source_code: str) -> str:
        """
        Main obfuscation method that must be implemented by subclasses.
        
        Args:
            source_code: The source code to obfuscate
            
        Returns:
            Obfuscated source code
        """
        pass
    
    def set_techniques(self, techniques: List[str]):
        """
        Set specific techniques to use instead of level-based defaults.
        
        Args:
            techniques: List of technique names to use
        """
        self.techniques = techniques
    
    def get_available_techniques(self) -> List[str]:
        """Get list of available techniques for this obfuscator."""
        return list(self.technique_map.keys())
    
    def generate_random_name(self, prefix: str = "_", length: int = 8) -> str:
        """
        Generate a random identifier name.
        
        Args:
            prefix: Prefix for the identifier
            length: Length of random part
            
        Returns:
            Random identifier name
        """
        if self.config.get('custom_encodings', {}).get('name_pattern') == 'hex':
            random_part = ''.join(random.choices('0123456789abcdef', k=length))
            return f"{prefix}0x{random_part}"
        else:
            # Default random pattern
            chars = string.ascii_letters + string.digits
            random_part = ''.join(random.choices(chars, k=length))
            return f"{prefix}{random_part}"
    
    def should_preserve(self, name: str) -> bool:
        """
        Check if a name should be preserved based on excluded patterns.
        
        Args:
            name: Name to check
            
        Returns:
            True if the name should be preserved
        """
        excluded = self.config.get('excluded_patterns', [])
        return any(pattern in name for pattern in excluded)
    
    def encode_string(self, text: str, method: str = 'default') -> str:
        """
        Encode a string using specified method.
        
        Args:
            text: Text to encode
            method: Encoding method ('base64', 'hex', 'char_codes', 'default')
            
        Returns:
            Encoded string representation
        """
        if method == 'base64':
            import base64
            encoded = base64.b64encode(text.encode()).decode()
            return f"__import__('base64').b64decode('{encoded}').decode()"
        
        elif method == 'hex':
            hex_str = text.encode().hex()
            return f"bytes.fromhex('{hex_str}').decode()"
        
        elif method == 'char_codes':
            char_codes = [str(ord(c)) for c in text]
            return f"''.join([chr({code}) for code in [{', '.join(char_codes)}]])"
        
        else:  # default - character concatenation
            chars = [f"chr({ord(c)})" for c in text]
            return f"''.join([{', '.join(chars)}])"
    
    def create_function_lookup(self, original_name: str, obfuscated_name: str) -> str:
        """
        Create a function lookup mechanism.
        
        Args:
            original_name: Original function name
            obfuscated_name: Obfuscated function name
            
        Returns:
            Code for function lookup
        """
        # This is a template - subclasses should override for language-specific implementation
        return f"{obfuscated_name} = globals().get('{original_name}')"
    
    def add_dead_code(self, code: str) -> str:
        """
        Add dead code segments for obfuscation.
        
        Args:
            code: Original code
            
        Returns:
            Code with dead code inserted
        """
        dead_code_snippets = [
            "# Dead code for obfuscation",
            "_ = 42 * 7 - 294",
            "__ = [i for i in range(10) if i % 2 == 0]",
            "___ = lambda x: x if x > 0 else -x",
        ]
        
        lines = code.split('\n')
        result = []
        
        for i, line in enumerate(lines):
            result.append(line)
            if i % 5 == 0 and line.strip():  # Add dead code every 5 lines
                result.append(random.choice(dead_code_snippets))
        
        return '\n'.join(result)
    
    def log_technique(self, technique_name: str, message: str):
        """
        Log technique application if verbose mode is enabled.
        
        Args:
            technique_name: Name of the technique being applied
            message: Log message
        """
        if self.config.get('verbose', False):
            print(f"[{technique_name}] {message}")
