"""
Control flow obfuscation techniques for Python code.
"""

import ast
import random
import re
from typing import Dict, List, Any, Optional


class ControlFlowObfuscator:
    """
    Handles control flow obfuscation techniques for Python code.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the control flow obfuscator.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.counter = 0
    
    def add_dummy_branches(self, code: str, context: Dict[str, Any]) -> str:
        """
        Add dummy conditional branches that don't affect execution.
        
        Args:
            code: Source code
            context: Obfuscation context
            
        Returns:
            Code with dummy branches
        """
        lines = code.split('\n')
        result = []
        
        for i, line in enumerate(lines):
            result.append(line)
            
            # Only add dummy branches in very safe locations
            if (random.random() < 0.05 and  # Reduced frequency
                line.strip() and 
                not line.strip().startswith('#') and
                not line.strip().startswith(('def ', 'class ', 'if ', 'for ', 'while ', 'try:', 'except', 'finally:', 'with ')) and
                not line.strip().endswith(':') and
                i < len(lines) - 1):  # Not the last line
                
                indent = len(line) - len(line.lstrip())
                dummy_condition = self._generate_dummy_condition()
                
                # Simple dummy branch that won't break anything
                dummy_branch = f"{' ' * indent}if {dummy_condition}: pass"
                result.append(dummy_branch)
        
        return '\n'.join(result)
    
    def add_opaque_predicates(self, code: str, context: Dict[str, Any]) -> str:
        """
        Add opaque predicates (conditions that always evaluate to true/false).
        
        Args:
            code: Source code
            context: Obfuscation context
            
        Returns:
            Code with opaque predicates
        """
        predicates_true = [
            "(7 * 6) == 42",
            "(10 % 3) == 1", 
            "len('test') == 4",
            "(5 + 5) > 9",
            "abs(-10) == 10",
        ]
        
        predicates_false = [
            "(2 + 2) == 5",
            "(10 % 3) == 0",
            "len('test') == 5", 
            "(5 + 5) < 9",
            "abs(-10) == -10",
        ]
        
        lines = code.split('\n')
        result = []
        
        for line in lines:
            result.append(line)
            
            if (random.random() < 0.1 and 
                line.strip() and 
                not line.strip().startswith('#')):
                
                indent = len(line) - len(line.lstrip())
                
                if random.choice([True, False]):
                    # Always true predicate
                    predicate = random.choice(predicates_true)
                    dummy_code = f"{' ' * indent}if not ({predicate}):\n{' ' * (indent + 4)}raise RuntimeError('Integrity check failed')"
                else:
                    # Always false predicate  
                    predicate = random.choice(predicates_false)
                    dummy_code = f"{' ' * indent}if {predicate}:\n{' ' * (indent + 4)}pass  # Never executed"
                
                result.append(dummy_code)
        
        return '\n'.join(result)
    
    def flatten_control_flow(self, code: str, context: Dict[str, Any]) -> str:
        """
        Flatten control flow using state machines.
        
        Args:
            code: Source code
            context: Obfuscation context
            
        Returns:
            Code with flattened control flow
        """
        # This is a simplified implementation of control flow flattening
        # A full implementation would require sophisticated CFG analysis
        
        try:
            tree = ast.parse(code)
            functions = self._find_functions(tree)
            
            if not functions:
                return code
            
            modified_code = code
            
            for func_node in functions:
                if self._should_flatten_function(func_node):
                    flattened = self._flatten_function(func_node)
                    # Replace in code (simplified)
                    # In practice, you'd need more sophisticated AST manipulation
                    modified_code = self._replace_function_in_code(modified_code, func_node, flattened)
            
            return modified_code
            
        except SyntaxError:
            return code
    
    def add_irrelevant_loops(self, code: str, context: Dict[str, Any]) -> str:
        """
        Add loops that don't affect the program logic.
        
        Args:
            code: Source code
            context: Obfuscation context
            
        Returns:
            Code with irrelevant loops
        """
        lines = code.split('\n')
        result = []
        
        for line in lines:
            result.append(line)
            
            if (random.random() < 0.08 and 
                line.strip() and 
                not line.strip().startswith('#')):
                
                indent = len(line) - len(line.lstrip())
                loop_var = f"_loop_{self.counter}"
                self.counter += 1
                
                # Add irrelevant loop
                irrelevant_loop = f"{' ' * indent}for {loop_var} in range(0):\n{' ' * (indent + 4)}pass  # Never executes"
                result.append(irrelevant_loop)
        
        return '\n'.join(result)
    
    def add_exception_obfuscation(self, code: str, context: Dict[str, Any]) -> str:
        """
        Add try-except blocks for obfuscation.
        
        Args:
            code: Source code
            context: Obfuscation context
            
        Returns:
            Code with exception-based obfuscation
        """
        lines = code.split('\n')
        result = []
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Occasionally wrap code blocks in try-except
            if (random.random() < 0.1 and 
                line.strip() and 
                not line.strip().startswith('#') and
                not line.strip().startswith('try:') and
                not line.strip().startswith('except')):
                
                indent = len(line) - len(line.lstrip())
                
                # Start try block
                result.append(f"{' ' * indent}try:")
                result.append(f"{' ' * (indent + 4)}{line.strip()}")
                
                # Look ahead for more lines to include
                j = i + 1
                while (j < len(lines) and 
                       j < i + 3 and  # Limit to 3 lines
                       lines[j].strip() and
                       not lines[j].strip().startswith('def ') and
                       not lines[j].strip().startswith('class ')):
                    result.append(f"{' ' * (indent + 4)}{lines[j].strip()}")
                    j += 1
                
                # Add except block that never catches
                result.append(f"{' ' * indent}except ImportError:")
                result.append(f"{' ' * (indent + 4)}pass  # Never reached")
                
                i = j
            else:
                result.append(line)
                i += 1
        
        return '\n'.join(result)
    
    def _generate_dummy_condition(self) -> str:
        """Generate a dummy condition."""
        conditions = [
            "True",
            "1 == 1", 
            "len([]) == 0",
            "'a' in 'abc'",
            "42 > 0",
            "bool(1)",
        ]
        return random.choice(conditions)
    
    def _find_functions(self, tree: ast.AST) -> List[ast.FunctionDef]:
        """Find all function definitions in AST."""
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node)
        return functions
    
    def _should_flatten_function(self, func_node: ast.FunctionDef) -> bool:
        """Determine if a function should be flattened."""
        # Only flatten small to medium functions
        return 5 <= len(func_node.body) <= 20
    
    def _flatten_function(self, func_node: ast.FunctionDef) -> str:
        """
        Flatten a function using state machine approach.
        
        This is a simplified implementation.
        """
        state_var = f"_state_{self.counter}"
        self.counter += 1
        
        flattened = f"""
def {func_node.name}({', '.join(arg.arg for arg in func_node.args.args)}):
    {state_var} = 0
    while True:
        if {state_var} == 0:
            # Original function body would be transformed here
            # This is a placeholder implementation
            {state_var} = 1
        elif {state_var} == 1:
            break
        else:
            break
"""
        return flattened
    
    def _replace_function_in_code(self, code: str, func_node: ast.FunctionDef, flattened: str) -> str:
        """Replace function in code with flattened version."""
        # This is a simplified implementation
        # In practice, you'd need to handle proper AST-to-code conversion
        pattern = rf"def\s+{re.escape(func_node.name)}\s*\([^)]*\):"
        
        # Find the function in the code and replace it
        # This is very basic and would need improvement for production use
        return re.sub(pattern, flattened.split('\n')[1], code, count=1)
