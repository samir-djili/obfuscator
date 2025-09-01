"""
Python-specific code obfuscator implementation.
"""

import ast
import re
import random
from typing import Dict, List, Any, Optional

from core.base_obfuscator import BaseObfuscator
from core.technique_manager import TechniqueManager
from .techniques.string_obfuscation import StringObfuscator
from .techniques.name_obfuscation import NameObfuscator
from .techniques.control_flow import ControlFlowObfuscator
from .techniques.dynamic_imports import DynamicImportObfuscator
from .techniques.bytecode_manipulation import BytecodeObfuscator


class PythonObfuscator(BaseObfuscator):
    """
    Python-specific code obfuscator with multiple obfuscation techniques.
    """
    
    def __init__(self, level: int = 2, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Python obfuscator.
        
        Args:
            level: Obfuscation level (1-4)
            config: Configuration dictionary
        """
        # Initialize technique classes first
        self.string_obfuscator = StringObfuscator(config)
        self.name_obfuscator = NameObfuscator(config)
        self.control_flow_obfuscator = ControlFlowObfuscator(config)
        self.dynamic_import_obfuscator = DynamicImportObfuscator(config)
        self.bytecode_obfuscator = BytecodeObfuscator(config)
        
        # Initialize technique manager
        self.technique_manager = TechniqueManager(config)
        
        # Context for maintaining state across techniques
        self.obfuscation_context = {}
        
        # Now call parent init which will call _init_techniques
        super().__init__(level, config)
    
    def _init_techniques(self):
        """Initialize available techniques for Python."""
        self.technique_map = {
            # Level 1 - Basic
            'string_encoding': self.string_obfuscator.encode_strings,
            'basic_name_change': self.name_obfuscator.basic_rename,
            'numeric_obfuscation': self._obfuscate_numbers,
            
            # Level 2 - Intermediate  
            'advanced_string_obfuscation': self.string_obfuscator.advanced_encoding,
            'function_name_obfuscation': self.name_obfuscator.obfuscate_functions,
            'variable_name_obfuscation': self.name_obfuscator.obfuscate_variables,
            'simple_control_flow': self.control_flow_obfuscator.add_dummy_branches,
            
            # Level 3 - Advanced
            'dynamic_string_assembly': self.string_obfuscator.dynamic_assembly,
            'control_flow_flattening': self.control_flow_obfuscator.flatten_control_flow,
            'dynamic_imports': self.dynamic_import_obfuscator.obfuscate_imports,
            'indirect_function_calls': self.name_obfuscator.indirect_calls,
            'dead_code_insertion': self._add_dead_code,
            
            # Level 4 - Expert
            'bytecode_manipulation': self.bytecode_obfuscator.manipulate_bytecode,
            'runtime_code_generation': self._runtime_generation,
            'anti_debugging': self._add_anti_debugging,
            'code_fragmentation': self._fragment_code,
        }
        
        # Register techniques with the technique manager
        for technique, func in self.technique_map.items():
            level = self._get_technique_level(technique)
            self.technique_manager.register_technique(technique, func, level)
    
    def _get_technique_level(self, technique: str) -> int:
        """Get the minimum level for a technique."""
        level_1 = ['string_encoding', 'basic_name_change', 'numeric_obfuscation']
        level_2 = ['advanced_string_obfuscation', 'function_name_obfuscation', 
                   'variable_name_obfuscation', 'simple_control_flow']
        level_3 = ['dynamic_string_assembly', 'control_flow_flattening', 
                   'dynamic_imports', 'indirect_function_calls', 'dead_code_insertion']
        level_4 = ['bytecode_manipulation', 'runtime_code_generation', 
                   'anti_debugging', 'code_fragmentation']
        
        if technique in level_1:
            return 1
        elif technique in level_2:
            return 2
        elif technique in level_3:
            return 3
        elif technique in level_4:
            return 4
        else:
            return 2  # default
    
    def obfuscate(self, source_code: str) -> str:
        """
        Main obfuscation method for Python code.
        
        Args:
            source_code: Python source code to obfuscate
            
        Returns:
            Obfuscated Python code
        """
        # Validate Python syntax
        try:
            ast.parse(source_code)
        except SyntaxError as e:
            raise ValueError(f"Invalid Python syntax: {e}")
        
        # Initialize obfuscation context
        self.obfuscation_context = {
            'original_code': source_code,
            'variable_mapping': {},
            'function_mapping': {},
            'string_mapping': {},
            'imports': [],
        }
        
        # Determine techniques to apply
        if self.techniques:
            # Use explicitly specified techniques
            techniques_to_apply = self.techniques
        else:
            # Use level-based techniques
            techniques_to_apply = self.technique_manager.get_techniques_for_level(self.level)
        
        # Apply techniques
        obfuscated_code = self.technique_manager.apply_techniques(
            source_code, 
            techniques_to_apply, 
            self.obfuscation_context
        )
        
        # Final cleanup and validation
        obfuscated_code = self._final_cleanup(obfuscated_code)
        
        return obfuscated_code
    
    def _obfuscate_numbers(self, code: str, context: Dict[str, Any]) -> str:
        """Obfuscate numeric literals."""
        def replace_number(match):
            num = int(match.group())
            if num == 0:
                return "(1-1)"
            elif num == 1:
                return "(2-1)"
            elif num > 1 and num < 100:
                # Create safe arithmetic expressions that always equal the original number
                operations = [
                    lambda x: f"({x//2}*2)" if x % 2 == 0 else f"({x//2}*2+1)",
                    lambda x: f"({x}+0)",  # Safe operation
                    lambda x: f"(int('{x}'))",
                ]
                return random.choice(operations)(num)
            else:
                return match.group()  # Keep large numbers as-is
        
        return re.sub(r'\b\d+\b', replace_number, code)
    
    def _add_dead_code(self, code: str, context: Dict[str, Any]) -> str:
        """Add dead code for obfuscation with proper syntax awareness."""
        lines = code.split('\n')
        result = []
        
        for i, line in enumerate(lines):
            result.append(line)
            
            # Only add dead code in safe locations
            if (line.strip() and 
                not line.strip().startswith('#') and 
                not line.strip().endswith(':') and  # Don't break blocks
                not line.strip().startswith(('import ', 'from ')) and
                random.random() < 0.05):  # Reduced frequency
                
                indent = len(line) - len(line.lstrip())
                
                # Safe dead code that won't break indentation
                safe_dead_code = [
                    f"pass  # {self.generate_random_name()}",
                    f"{self.generate_random_name()} = None",
                    f"_ = {random.randint(1, 100)}",
                ]
                
                dead_line = ' ' * indent + random.choice(safe_dead_code)
                result.append(dead_line)
        
        return '\n'.join(result)
    
    def _runtime_generation(self, code: str, context: Dict[str, Any]) -> str:
        """Add runtime code generation techniques."""
        # Add exec/eval based obfuscation for level 4
        runtime_header = f'''
# Runtime code generation setup
{self.generate_random_name()} = compile
{self.generate_random_name()} = exec
{self.generate_random_name()} = eval
'''
        return runtime_header + code
    
    def _add_anti_debugging(self, code: str, context: Dict[str, Any]) -> str:
        """Add anti-debugging techniques."""
        anti_debug_code = f'''
# Anti-debugging checks
import sys
import os
{self.generate_random_name()} = lambda: sys.gettrace() is None or os._exit(1)
{self.generate_random_name()}()
'''
        return anti_debug_code + code
    
    def _fragment_code(self, code: str, context: Dict[str, Any]) -> str:
        """Fragment code into multiple parts."""
        lines = code.split('\n')
        
        # Group lines into fragments
        fragments = []
        current_fragment = []
        
        for line in lines:
            current_fragment.append(line)
            if len(current_fragment) >= 5:  # Fragment every 5 lines
                fragments.append('\n'.join(current_fragment))
                current_fragment = []
        
        if current_fragment:
            fragments.append('\n'.join(current_fragment))
        
        # Create fragment execution system
        fragment_vars = []
        fragment_setup = []
        
        for i, fragment in enumerate(fragments):
            var_name = self.generate_random_name()
            fragment_vars.append(var_name)
            encoded_fragment = self.encode_string(fragment, 'base64')
            fragment_setup.append(f"{var_name} = {encoded_fragment}")
        
        execution_code = f'''
# Code fragmentation system
{"_nl_".join(fragment_setup)}

# Execute fragments
for {self.generate_random_name()} in [{", ".join(fragment_vars)}]:
    exec({self.generate_random_name()})
'''
        return execution_code
    
    def _final_cleanup(self, code: str) -> str:
        """Perform final cleanup and validation."""
        # Remove excessive whitespace
        lines = code.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Skip empty lines that might break Python syntax
            if line.strip() or (cleaned_lines and cleaned_lines[-1].strip()):
                cleaned_lines.append(line)
        
        cleaned_code = '\n'.join(cleaned_lines)
        
        # Try to validate syntax
        try:
            ast.parse(cleaned_code)
        except SyntaxError as e:
            # If syntax is broken, return with minimal obfuscation
            print(f"Warning: Syntax validation failed ({e}), using fallback obfuscation")
            return self._apply_basic_fallback(self.obfuscation_context['original_code'])
        
        return cleaned_code
    
    def _apply_basic_fallback(self, code: str) -> str:
        """Apply basic obfuscation as fallback."""
        # Simple string encoding only
        return self.string_obfuscator.encode_strings(code, {})
