"""
Dynamic import obfuscation techniques for Python code.
"""

import re
import ast
import random
from typing import Dict, List, Any, Optional, Set


class DynamicImportObfuscator:
    """
    Handles dynamic import obfuscation techniques for Python code.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the dynamic import obfuscator.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.import_mapping = {}
        self.alias_mapping = {}  # Track original name -> obfuscated alias
        self.counter = 0
    
    def _generate_alias_name(self) -> str:
        """Generate obfuscated alias name."""
        import string
        import random
        length = random.randint(8, 12)
        name = ''.join(random.choices(string.ascii_letters + '_', k=length))
        # Ensure it starts with a letter or underscore
        if name[0].isdigit():
            name = '_' + name[1:]
        return name
    
    def obfuscate_imports(self, code: str, context: Dict[str, Any]) -> str:
        """
        Obfuscate import statements using dynamic imports.
        
        Args:
            code: Source code
            context: Obfuscation context
            
        Returns:
            Code with obfuscated imports
        """
        # Use regex-based approach for better reliability
        result = self._regex_based_import_obfuscation(code)
        
        # Now replace all references to the original import names with obfuscated aliases
        for original_name, obfuscated_alias in self.alias_mapping.items():
            # Use word boundaries to replace only complete identifiers
            pattern = rf'\b{re.escape(original_name)}\b'
            result = re.sub(pattern, obfuscated_alias, result)
        
        # Store alias mapping in context for other techniques to use
        if 'alias_mapping' not in context:
            context['alias_mapping'] = {}
        context['alias_mapping'].update(self.alias_mapping)
        
        # Extract module names and add them to reserved names to prevent further obfuscation
        import_lines = [line.strip() for line in code.split('\n') if line.strip().startswith(('import ', 'from '))]
        reserved_modules = set()
        reserved_items = set()
        
        for line in import_lines:
            # Extract module names from import statements
            if line.startswith('import '):
                match = re.match(r'import\s+(\w+)', line)
                if match:
                    reserved_modules.add(match.group(1))
            elif line.startswith('from '):
                # Extract both module and imported items
                match = re.match(r'from\s+(\w+)\s+import\s+(.+)', line)
                if match:
                    module = match.group(1)
                    items = match.group(2)
                    reserved_modules.add(module)
                    
                    # Parse imported items
                    for item in items.split(','):
                        item = item.strip()
                        if ' as ' in item:
                            orig, alias = item.split(' as ', 1)
                            reserved_items.add(orig.strip())
                            reserved_items.add(alias.strip())
                        else:
                            reserved_items.add(item)
        
        # Add obfuscated aliases to reserved names so they don't get re-obfuscated
        reserved_items.update(self.alias_mapping.values())
        
        # Add to context for other techniques to respect
        if 'reserved_names' not in context:
            context['reserved_names'] = set()
        context['reserved_names'].update(reserved_modules)
        context['reserved_names'].update(reserved_items)
        
        return result
    
    def obfuscate_from_imports(self, code: str, context: Dict[str, Any]) -> str:
        """
        Specifically obfuscate 'from ... import ...' statements.
        
        Args:
            code: Source code
            context: Obfuscation context
            
        Returns:
            Code with obfuscated from imports
        """
        from_import_pattern = r'from\s+(\w+(?:\.\w+)*)\s+import\s+([^#\n]+)'
        
        def replace_from_import(match):
            module = match.group(1)
            items = match.group(2)
            
            # Create dynamic equivalent
            var_name = f"_mod_{self.counter}"
            self.counter += 1
            
            replacement = f"{var_name} = __import__('{module}')\n"
            
            # Handle multiple imports
            item_list = [item.strip() for item in items.split(',')]
            for item in item_list:
                if ' as ' in item:
                    orig, alias = item.split(' as ', 1)
                    replacement += f"{alias.strip()} = getattr({var_name}, '{orig.strip()}')\n"
                else:
                    replacement += f"{item.strip()} = getattr({var_name}, '{item.strip()}')\n"
            
            return replacement.rstrip()
        
        return re.sub(from_import_pattern, replace_from_import, code)
    
    def create_import_proxy(self, code: str, context: Dict[str, Any]) -> str:
        """
        Create proxy functions for imports.
        
        Args:
            code: Source code
            context: Obfuscation context
            
        Returns:
            Code with import proxies
        """
        # Create a generic import proxy function
        proxy_name = f"_import_proxy_{self.counter}"
        self.counter += 1
        
        proxy_code = f"""
def {proxy_name}(module_name, from_list=None):
    if from_list:
        module = __import__(module_name, fromlist=from_list)
        return {{item: getattr(module, item) for item in from_list}}
    else:
        return __import__(module_name)

"""
        
        # Replace import statements with proxy calls
        import_pattern = r'^import\s+(\w+(?:\.\w+)*)(?:\s+as\s+(\w+))?$'
        from_import_pattern = r'^from\s+(\w+(?:\.\w+)*)\s+import\s+([^#\n]+)$'
        
        def replace_import(match):
            module = match.group(1)
            alias = match.group(2)
            
            if alias:
                return f"{alias} = {proxy_name}('{module}')"
            else:
                return f"{module.split('.')[-1]} = {proxy_name}('{module}')"
        
        def replace_from_import(match):
            module = match.group(1)
            items = match.group(2)
            
            item_list = [item.strip() for item in items.split(',')]
            result = f"_imported = {proxy_name}('{module}', {item_list})\n"
            
            for item in item_list:
                if ' as ' in item:
                    orig, alias = item.split(' as ', 1)
                    result += f"{alias.strip()} = _imported['{orig.strip()}']\n"
                else:
                    result += f"{item.strip()} = _imported['{item.strip()}']\n"
            
            return result.rstrip()
        
        modified_code = re.sub(import_pattern, replace_import, code, flags=re.MULTILINE)
        modified_code = re.sub(from_import_pattern, replace_from_import, modified_code, flags=re.MULTILINE)
        
        return proxy_code + modified_code
    
    def lazy_imports(self, code: str, context: Dict[str, Any]) -> str:
        """
        Convert imports to lazy loading pattern.
        
        Args:
            code: Source code
            context: Obfuscation context
            
        Returns:
            Code with lazy imports
        """
        lazy_loader_name = f"_lazy_{self.counter}"
        self.counter += 1
        
        lazy_loader = f"""
class {lazy_loader_name}:
    def __init__(self):
        self._modules = {{}}
    
    def get(self, name):
        if name not in self._modules:
            self._modules[name] = __import__(name)
        return self._modules[name]

{lazy_loader_name}_instance = {lazy_loader_name}()

"""
        
        # Replace import statements with lazy loader calls
        import_pattern = r'^import\s+(\w+(?:\.\w+)*)(?:\s+as\s+(\w+))?$'
        
        def replace_with_lazy(match):
            module = match.group(1)
            alias = match.group(2)
            
            var_name = alias or module.split('.')[-1]
            return f"{var_name} = {lazy_loader_name}_instance.get('{module}')"
        
        modified_code = re.sub(import_pattern, replace_with_lazy, code, flags=re.MULTILINE)
        
        return lazy_loader + modified_code
    
    def _collect_imports(self, tree: ast.AST) -> Dict[str, Any]:
        """Collect all import statements from AST."""
        imports = {
            'regular': [],  # import module
            'from': [],     # from module import item
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports['regular'].append({
                        'module': alias.name,
                        'alias': alias.asname
                    })
            elif isinstance(node, ast.ImportFrom):
                import_info = {
                    'module': node.module,
                    'items': []
                }
                for alias in node.names:
                    import_info['items'].append({
                        'name': alias.name,
                        'alias': alias.asname
                    })
                imports['from'].append(import_info)
        
        return imports
    
    def _create_dynamic_imports(self, imports: Dict[str, Any]) -> str:
        """Create dynamic import statements."""
        dynamic_code = []
        
        # Handle regular imports
        for imp in imports['regular']:
            module = imp['module']
            alias = imp['alias'] or module.split('.')[-1]
            
            dynamic_code.append(f"{alias} = __import__('{module}')")
        
        # Handle from imports
        for imp in imports['from']:
            module = imp['module']
            temp_var = f"_temp_mod_{self.counter}"
            self.counter += 1
            
            dynamic_code.append(f"{temp_var} = __import__('{module}')")
            
            for item in imp['items']:
                name = item['name']
                alias = item['alias'] or name
                dynamic_code.append(f"{alias} = getattr({temp_var}, '{name}')")
        
        return '\n'.join(dynamic_code)
    
    def _replace_imports(self, code: str, imports: Dict[str, Any], dynamic_imports: str) -> str:
        """Replace original imports with dynamic versions."""
        lines = code.split('\n')
        result = []
        
        # Add dynamic imports at the beginning
        if dynamic_imports:
            result.append("# Dynamic imports")
            result.append(dynamic_imports)
            result.append("")
        
        # Filter out original import statements
        for line in lines:
            stripped = line.strip()
            if not (stripped.startswith('import ') or stripped.startswith('from ')):
                result.append(line)
        
        return '\n'.join(result)
    
    def _regex_based_import_obfuscation(self, code: str) -> str:
        """Improved regex-based import obfuscation with string obfuscation and alias obfuscation."""
        lines = code.split('\n')
        result = []
        
        for line in lines:
            stripped = line.strip()
            
            # Handle regular imports: import module, import module as alias
            import_match = re.match(r'^import\s+(\w+(?:\.\w+)*)(?:\s+as\s+(\w+))?$', stripped)
            if import_match:
                module = import_match.group(1)
                original_alias = import_match.group(2) or module.split('.')[-1]
                
                # Generate obfuscated alias
                obfuscated_alias = self._generate_alias_name()
                self.alias_mapping[original_alias] = obfuscated_alias
                
                obfuscated_module = self._obfuscate_string(module)
                result.append(f"{obfuscated_alias} = __import__({obfuscated_module})")
                continue
            
            # Handle from imports: from module import item, from module import item as alias
            from_match = re.match(r'^from\s+(\w+(?:\.\w+)*)\s+import\s+(\w+)(?:\s+as\s+(\w+))?$', stripped)
            if from_match:
                module = from_match.group(1)
                item = from_match.group(2)
                original_alias = from_match.group(3) or item
                
                # Generate obfuscated alias
                obfuscated_alias = self._generate_alias_name()
                self.alias_mapping[original_alias] = obfuscated_alias
                
                obfuscated_module = self._obfuscate_string(module)
                obfuscated_item = self._obfuscate_string(item)
                result.append(f"{obfuscated_alias} = getattr(__import__({obfuscated_module}), {obfuscated_item})")
                continue
            
            # Handle multiple from imports: from module import item1, item2
            multi_from_match = re.match(r'^from\s+(\w+(?:\.\w+)*)\s+import\s+([^#\n]+)$', stripped)
            if multi_from_match and ',' in multi_from_match.group(2):
                module = multi_from_match.group(1)
                items = [item.strip() for item in multi_from_match.group(2).split(',')]
                obfuscated_module = self._obfuscate_string(module)
                
                for item in items:
                    if ' as ' in item:
                        orig, original_alias = item.split(' as ', 1)
                        original_alias = original_alias.strip()
                        obfuscated_alias = self._generate_alias_name()
                        self.alias_mapping[original_alias] = obfuscated_alias
                        obfuscated_item = self._obfuscate_string(orig.strip())
                        result.append(f"{obfuscated_alias} = getattr(__import__({obfuscated_module}), {obfuscated_item})")
                    else:
                        obfuscated_alias = self._generate_alias_name()
                        self.alias_mapping[item] = obfuscated_alias
                        obfuscated_item = self._obfuscate_string(item)
                        result.append(f"{obfuscated_alias} = getattr(__import__({obfuscated_module}), {obfuscated_item})")
                continue
            
            # Keep non-import lines as-is
            result.append(line)
        
        return '\n'.join(result)
    
    def _obfuscate_string(self, text: str) -> str:
        """Obfuscate a string using character codes."""
        char_codes = [str(ord(char)) for char in text]
        return f"''.join([chr(char_code) for char_code in [{', '.join(char_codes)}]])"
