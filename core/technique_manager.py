"""
Technique manager for organizing and applying obfuscation techniques.
"""

from typing import Dict, List, Any, Optional, Callable
from enum import Enum


class ObfuscationLevel(Enum):
    """Enumeration of obfuscation levels."""
    BASIC = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    EXPERT = 4


class TechniqueManager:
    """
    Manages obfuscation techniques and their application order.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the technique manager.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.techniques: Dict[str, Callable] = {}
        self.level_mappings: Dict[int, List[str]] = {
            1: [],  # Basic techniques
            2: [],  # Intermediate techniques
            3: [],  # Advanced techniques
            4: [],  # Expert techniques
        }
        self.dependencies: Dict[str, List[str]] = {}
        self.conflicts: Dict[str, List[str]] = {}
    
    def register_technique(self, 
                          name: str, 
                          func: Callable, 
                          level: int, 
                          dependencies: Optional[List[str]] = None,
                          conflicts: Optional[List[str]] = None):
        """
        Register a new obfuscation technique.
        
        Args:
            name: Technique name
            func: Function that implements the technique
            level: Minimum obfuscation level for this technique
            dependencies: List of techniques that must run before this one
            conflicts: List of techniques that cannot run with this one
        """
        self.techniques[name] = func
        
        # Add to appropriate levels
        for lvl in range(level, 5):
            if name not in self.level_mappings[lvl]:
                self.level_mappings[lvl].append(name)
        
        if dependencies:
            self.dependencies[name] = dependencies
        
        if conflicts:
            self.conflicts[name] = conflicts
    
    def get_techniques_for_level(self, level: int) -> List[str]:
        """
        Get all techniques available for a given obfuscation level.
        
        Args:
            level: Obfuscation level (1-4)
            
        Returns:
            List of technique names
        """
        return self.level_mappings.get(level, [])
    
    def resolve_dependencies(self, techniques: List[str]) -> List[str]:
        """
        Resolve technique dependencies and return ordered list.
        
        Args:
            techniques: List of technique names to execute
            
        Returns:
            Ordered list of techniques with dependencies resolved
        """
        resolved = []
        visited = set()
        temp_visited = set()
        
        def visit(technique: str):
            if technique in temp_visited:
                raise ValueError(f"Circular dependency detected involving {technique}")
            
            if technique in visited:
                return
            
            temp_visited.add(technique)
            
            # Visit dependencies first
            deps = self.dependencies.get(technique, [])
            for dep in deps:
                if dep in techniques:  # Only include dependencies that are actually requested
                    visit(dep)
            
            temp_visited.remove(technique)
            visited.add(technique)
            
            if technique not in resolved:
                resolved.append(technique)
        
        for technique in techniques:
            visit(technique)
        
        return resolved
    
    def check_conflicts(self, techniques: List[str]) -> List[str]:
        """
        Check for conflicts between techniques.
        
        Args:
            techniques: List of technique names
            
        Returns:
            List of conflict descriptions
        """
        conflicts = []
        
        for technique in techniques:
            conflicting = self.conflicts.get(technique, [])
            for conflict in conflicting:
                if conflict in techniques:
                    conflicts.append(f"{technique} conflicts with {conflict}")
        
        return conflicts
    
    def apply_techniques(self, 
                        code: str, 
                        techniques: List[str],
                        context: Optional[Dict[str, Any]] = None) -> str:
        """
        Apply a list of techniques to code in the correct order.
        
        Args:
            code: Source code to obfuscate
            techniques: List of technique names to apply
            context: Optional context dictionary for techniques
            
        Returns:
            Obfuscated code
        """
        if not techniques:
            return code
        
        # Check for conflicts
        conflicts = self.check_conflicts(techniques)
        if conflicts:
            raise ValueError(f"Technique conflicts detected: {'; '.join(conflicts)}")
        
        # Resolve dependencies
        ordered_techniques = self.resolve_dependencies(techniques)
        
        # Apply techniques in order
        result = code
        applied_context = context or {}
        
        for technique_name in ordered_techniques:
            if technique_name not in self.techniques:
                raise ValueError(f"Unknown technique: {technique_name}")
            
            technique_func = self.techniques[technique_name]
            
            # Apply the technique
            try:
                before_len = len(result)
                result = technique_func(result, applied_context)
                after_len = len(result)
                applied_context[f"{technique_name}_applied"] = True
                
                print(f"Applied technique: {technique_name} (size: {before_len} -> {after_len})")
                    
            except Exception as e:
                print(f"ERROR: Technique {technique_name} failed: {e}")
                if self.config.get('strict_mode', False):
                    raise RuntimeError(f"Technique {technique_name} failed: {e}")
        
        return result
    
    def get_technique_info(self, technique_name: str) -> Dict[str, Any]:
        """
        Get information about a specific technique.
        
        Args:
            technique_name: Name of the technique
            
        Returns:
            Dictionary with technique information
        """
        if technique_name not in self.techniques:
            return {}
        
        levels = [level for level, techs in self.level_mappings.items() 
                 if technique_name in techs]
        
        return {
            'name': technique_name,
            'levels': levels,
            'min_level': min(levels) if levels else None,
            'dependencies': self.dependencies.get(technique_name, []),
            'conflicts': self.conflicts.get(technique_name, []),
            'function': self.techniques[technique_name]
        }
    
    def list_all_techniques(self) -> Dict[str, Dict[str, Any]]:
        """
        Get information about all registered techniques.
        
        Returns:
            Dictionary mapping technique names to their information
        """
        return {name: self.get_technique_info(name) 
                for name in self.techniques.keys()}
    
    def suggest_techniques(self, level: int, exclude: Optional[List[str]] = None) -> List[str]:
        """
        Suggest techniques for a given level, excluding conflicting ones.
        
        Args:
            level: Obfuscation level
            exclude: List of techniques to exclude
            
        Returns:
            List of suggested technique names
        """
        available = self.get_techniques_for_level(level)
        exclude = exclude or []
        
        suggested = []
        for technique in available:
            if technique in exclude:
                continue
            
            # Check if any conflicts are already in suggested list
            conflicts = self.conflicts.get(technique, [])
            if any(conflict in suggested for conflict in conflicts):
                continue
            
            suggested.append(technique)
        
        return suggested
