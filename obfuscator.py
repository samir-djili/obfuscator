#!/usr/bin/env python3
"""
Code Obfuscator - Main CLI Entry Point

A powerful, modular code obfuscation tool supporting multiple programming languages.
"""

import argparse
import sys
import os
import json
from pathlib import Path

from core.language_detector import LanguageDetector
from core.technique_manager import TechniqueManager
from languages.python.obfuscator import PythonObfuscator


def load_config(config_path=None):
    """Load configuration from file or use defaults."""
    default_config = {
        "default_level": 2,
        "preserve_functionality": True,
        "randomize_seeds": True,
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
    
    if config_path and os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        except Exception as e:
            print(f"Warning: Could not load config file: {e}")
    
    return default_config


def get_obfuscator(language, level, config):
    """Factory function to get the appropriate obfuscator."""
    obfuscator_map = {
        'python': PythonObfuscator,
        # Future languages will be added here
        # 'javascript': JavaScriptObfuscator,
        # 'java': JavaObfuscator,
    }
    
    if language not in obfuscator_map:
        raise ValueError(f"Unsupported language: {language}. Supported: {list(obfuscator_map.keys())}")
    
    return obfuscator_map[language](level=level, config=config)


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Advanced code obfuscation tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python obfuscator.py --input file.py --output obfuscated.py
  python obfuscator.py --input file.py --output obfuscated.py --level 3
  python obfuscator.py --input file.py --output obfuscated.py --techniques string_encoding,control_flow
  python obfuscator.py --input file.py --output obfuscated.py --randomize --verbose
        """
    )
    
    # Required arguments
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Input file to obfuscate'
    )
    
    parser.add_argument(
        '--output', '-o',
        required=True,
        help='Output file for obfuscated code'
    )
    
    # Optional arguments
    parser.add_argument(
        '--language', '-l',
        help='Programming language (auto-detected if not specified)'
    )
    
    parser.add_argument(
        '--level',
        type=int,
        choices=[1, 2, 3, 4],
        default=2,
        help='Obfuscation level (1=basic, 2=intermediate, 3=advanced, 4=expert)'
    )
    
    parser.add_argument(
        '--techniques', '-t',
        help='Comma-separated list of specific techniques to use'
    )
    
    parser.add_argument(
        '--randomize', '-r',
        action='store_true',
        help='Randomize obfuscation patterns for better security'
    )
    
    parser.add_argument(
        '--config', '-c',
        help='Path to configuration file'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be obfuscated without writing output'
    )
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' does not exist.")
        sys.exit(1)
    
    # Load configuration
    config = load_config(args.config)
    
    # Update config with command line arguments
    if args.randomize:
        config['randomize_seeds'] = True
    
    try:
        # Read input file
        with open(args.input, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        if args.verbose:
            print(f"Read {len(source_code)} characters from {args.input}")
        
        # Detect language if not specified
        language = args.language
        if not language:
            detector = LanguageDetector()
            language = detector.detect(args.input, source_code)
            if args.verbose:
                print(f"Detected language: {language}")
        
        # Get specific techniques if provided
        techniques = None
        if args.techniques:
            techniques = [t.strip() for t in args.techniques.split(',')]
            if args.verbose:
                print(f"Using techniques: {techniques}")
        
        # Get obfuscator
        obfuscator = get_obfuscator(language, args.level, config)
        
        # Set specific techniques if provided
        if techniques:
            obfuscator.set_techniques(techniques)
        
        if args.verbose:
            print(f"Using {language} obfuscator with level {args.level}")
            print("Starting obfuscation...")
        
        # Perform obfuscation
        obfuscated_code = obfuscator.obfuscate(source_code)
        
        if args.dry_run:
            print("Dry run - obfuscation complete. Output preview:")
            print("-" * 50)
            print(obfuscated_code[:500] + "..." if len(obfuscated_code) > 500 else obfuscated_code)
            print("-" * 50)
        else:
            # Write output file
            os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(obfuscated_code)
            
            if args.verbose:
                print(f"Obfuscated code written to {args.output}")
                print(f"Original size: {len(source_code)} characters")
                print(f"Obfuscated size: {len(obfuscated_code)} characters")
        
        print("Obfuscation completed successfully!")
        
    except Exception as e:
        print(f"Error during obfuscation: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
