"""
Language detection utilities for automatic language identification.
"""

import os
import re
from typing import Dict, List, Optional


class LanguageDetector:
    """
    Detects programming languages based on file extensions and content analysis.
    """
    
    def __init__(self):
        """Initialize the language detector with known patterns."""
        self.extension_map = {
            '.py': 'python',
            '.pyw': 'python',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript',
            '.java': 'java',
            '.class': 'java',
            '.cpp': 'cpp',
            '.cc': 'cpp',
            '.cxx': 'cpp',
            '.c++': 'cpp',
            '.c': 'c',
            '.h': 'c',
            '.hpp': 'cpp',
            '.cs': 'csharp',
            '.php': 'php',
            '.rb': 'ruby',
            '.go': 'go',
            '.rs': 'rust',
            '.kt': 'kotlin',
            '.scala': 'scala',
            '.swift': 'swift',
        }
        
        # Content-based patterns for language detection
        self.content_patterns = {
            'python': [
                r'def\s+\w+\s*\(',
                r'import\s+\w+',
                r'from\s+\w+\s+import',
                r'if\s+__name__\s*==\s*["\']__main__["\']',
                r'print\s*\(',
                r'class\s+\w+\s*\(',
            ],
            'javascript': [
                r'function\s+\w+\s*\(',
                r'var\s+\w+\s*=',
                r'let\s+\w+\s*=',
                r'const\s+\w+\s*=',
                r'console\.log\s*\(',
                r'=>',
            ],
            'java': [
                r'public\s+class\s+\w+',
                r'public\s+static\s+void\s+main',
                r'import\s+java\.',
                r'System\.out\.print',
                r'@\w+',
                r'new\s+\w+\s*\(',
            ],
            'cpp': [
                r'#include\s*<\w+>',
                r'int\s+main\s*\(',
                r'std::\w+',
                r'cout\s*<<',
                r'cin\s*>>',
                r'namespace\s+\w+',
            ],
            'c': [
                r'#include\s*<\w+\.h>',
                r'int\s+main\s*\(',
                r'printf\s*\(',
                r'scanf\s*\(',
                r'malloc\s*\(',
                r'free\s*\(',
            ]
        }
    
    def detect_by_extension(self, filename: str) -> Optional[str]:
        """
        Detect language based on file extension.
        
        Args:
            filename: Path to the file
            
        Returns:
            Detected language or None if unknown
        """
        _, ext = os.path.splitext(filename.lower())
        return self.extension_map.get(ext)
    
    def detect_by_content(self, content: str) -> Optional[str]:
        """
        Detect language based on content analysis.
        
        Args:
            content: Source code content
            
        Returns:
            Detected language or None if uncertain
        """
        scores = {}
        
        for language, patterns in self.content_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, content, re.MULTILINE | re.IGNORECASE))
                score += matches
            
            if score > 0:
                scores[language] = score
        
        if not scores:
            return None
        
        # Return language with highest score
        return max(scores, key=scores.get)
    
    def detect(self, filename: str, content: str = None) -> str:
        """
        Detect programming language using both filename and content.
        
        Args:
            filename: Path to the file
            content: Optional file content for analysis
            
        Returns:
            Detected language (defaults to 'python' if uncertain)
        """
        # First try extension-based detection
        lang_by_ext = self.detect_by_extension(filename)
        
        # If content is available, also try content-based detection
        lang_by_content = None
        if content:
            lang_by_content = self.detect_by_content(content)
        
        # Priority: extension match, then content match, then default to python
        if lang_by_ext:
            return lang_by_ext
        elif lang_by_content:
            return lang_by_content
        else:
            # Default to python if detection fails
            return 'python'
    
    def get_supported_languages(self) -> List[str]:
        """
        Get list of languages that have detection patterns.
        
        Returns:
            List of supported language names
        """
        extensions_langs = set(self.extension_map.values())
        content_langs = set(self.content_patterns.keys())
        return sorted(extensions_langs.union(content_langs))
    
    def get_extensions_for_language(self, language: str) -> List[str]:
        """
        Get file extensions associated with a language.
        
        Args:
            language: Programming language name
            
        Returns:
            List of file extensions for the language
        """
        return [ext for ext, lang in self.extension_map.items() if lang == language]
