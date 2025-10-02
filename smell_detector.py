#!/usr/bin/env python3
"""
Code Smell Detection Application
Detects 6 common code smells in Python source code
"""

import ast
import os
import sys
import argparse
import yaml
from pathlib import Path
from typing import List, Dict, Any, Set
import re

class CodeSmellDetector:
    def __init__(self):
        self.smell_handlers = {
            'LongMethod': self.detect_long_methods,
            'GodClass': self.detect_god_classes,
            'DuplicatedCode': self.detect_duplicated_code,
            'LargeParameterList': self.detect_large_parameter_lists,
            'MagicNumbers': self.detect_magic_numbers,
            'FeatureEnvy': self.detect_feature_envy
        }
        
        self.config = {
            'LongMethod': {'enabled': True, 'max_lines': 20},
            'GodClass': {'enabled': True, 'max_methods': 8, 'max_attrs': 6},
            'DuplicatedCode': {'enabled': True, 'min_duplication_lines': 5},
            'LargeParameterList': {'enabled': True, 'max_parameters': 5},
            'MagicNumbers': {'enabled': True, 'excluded_numbers': [0, 1, -1, 100]},
            'FeatureEnvy': {'enabled': True}
        }
    
    def load_config(self, config_path: str) -> None:
        """Load configuration from YAML file"""
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                user_config = yaml.safe_load(f) or {}
                for smell, settings in user_config.items():
                    if smell in self.config:
                        self.config[smell].update(settings)
    
    def update_config_from_cli(self, only_smells: List[str] = None, exclude_smells: List[str] = None) -> None:
        """Update configuration based on CLI flags"""
        if only_smells:
            for smell in self.config:
                self.config[smell]['enabled'] = smell in only_smells
        elif exclude_smells:
            for smell in exclude_smells:
                if smell in self.config:
                    self.config[smell]['enabled'] = False
    
    def detect_smells(self, file_path: str) -> Dict[str, List[Dict]]:
        """Main method to detect all enabled code smells"""
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        try:
            tree = ast.parse(source_code)
        except SyntaxError as e:
            return {'error': f'Syntax error in {file_path}: {e}'}
        
        smells_found = {}
        
        for smell_name, handler in self.smell_handlers.items():
            if self.config[smell_name]['enabled']:
                smells_found[smell_name] = handler(tree, source_code, file_path)
        
        return smells_found
    
    def detect_long_methods(self, tree: ast.AST, source_code: str, file_path: str) -> List[Dict]:
        """Detect methods longer than configured threshold"""
        long_methods = []
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Calculate method length by counting lines
                start_line = node.lineno
                end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line
                method_length = end_line - start_line + 1
                
                if method_length > self.config['LongMethod']['max_lines']:
                    long_methods.append({
                        'name': node.name,
                        'line_range': f"{start_line}-{end_line}",
                        'length': method_length,
                        'file': file_path
                    })
        
        return long_methods
    
    def detect_god_classes(self, tree: ast.AST, source_code: str, file_path: str) -> List[Dict]:
        """Detect classes with too many methods and attributes"""
        god_classes = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                methods = []
                attributes = []
                
                # Count methods and class-level assignments
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        methods.append(item.name)
                    elif isinstance(item, ast.Assign):
                        for target in item.targets:
                            if isinstance(target, ast.Name):
                                attributes.append(target.id)
                
                total_methods = len(methods)
                total_attributes = len(attributes)
                
                if (total_methods > self.config['GodClass']['max_methods'] or 
                    total_attributes > self.config['GodClass']['max_attrs']):
                    god_classes.append({
                        'name': node.name,
                        'line_range': f"{node.lineno}-{node.end_lineno}",
                        'methods_count': total_methods,
                        'attributes_count': total_attributes,
                        'file': file_path
                    })
        
        return god_classes
    
    def detect_duplicated_code(self, tree: ast.AST, source_code: str, file_path: str) -> List[Dict]:
        """Detect duplicated code blocks using simple pattern matching"""
        lines = source_code.split('\n')
        duplicates = []
        min_lines = self.config['DuplicatedCode']['min_duplication_lines']
        
        # Simple line-based duplication detection
        for i in range(len(lines) - min_lines):
            block = '\n'.join(lines[i:i + min_lines]).strip()
            if not block or len(block.split('\n')) < min_lines:
                continue
            
            # Look for identical blocks later in the file
            for j in range(i + min_lines, len(lines) - min_lines):
                compare_block = '\n'.join(lines[j:j + min_lines]).strip()
                if block == compare_block and block:
                    duplicates.append({
                        'line_range_1': f"{i+1}-{i+min_lines}",
                        'line_range_2': f"{j+1}-{j+min_lines}",
                        'file': file_path,
                        'sample': block[:100] + '...' if len(block) > 100 else block
                    })
                    break  # Avoid reporting the same block multiple times
        
        return duplicates[:10]  # Limit results to avoid overwhelming output
    
    def detect_large_parameter_lists(self, tree: ast.AST, source_code: str, file_path: str) -> List[Dict]:
        """Detect functions with too many parameters"""
        large_params = []
        max_params = self.config['LargeParameterList']['max_parameters']
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Count parameters (excluding self/cls)
                args = node.args
                param_count = len(args.args) + len(args.kwonlyargs)
                
                if hasattr(args, 'vararg') and args.vararg:
                    param_count += 1
                if hasattr(args, 'kwarg') and args.kwarg:
                    param_count += 1
                
                # Subtract 1 for self in methods
                if param_count > 0 and node.args.args and node.args.args[0].arg in ('self', 'cls'):
                    param_count -= 1
                
                if param_count > max_params:
                    large_params.append({
                        'name': node.name,
                        'line': node.lineno,
                        'parameter_count': param_count,
                        'file': file_path
                    })
        
        return large_params
    
    def detect_magic_numbers(self, tree: ast.AST, source_code: str, file_path: str) -> List[Dict]:
        """Detect magic numbers in the code"""
        magic_numbers = []
        excluded = set(self.config['MagicNumbers']['excluded_numbers'])
        
        # Pattern to find numbers in source code (integers and floats)
        number_pattern = r'\b(-?\d+\.?\d*)\b'
        
        lines = source_code.split('\n')
        for line_num, line in enumerate(lines, 1):
            numbers = re.findall(number_pattern, line)
            for num_str in numbers:
                try:
                    # Try to convert to int or float
                    if '.' in num_str:
                        num = float(num_str)
                    else:
                        num = int(num_str)
                    
                    # Check if it's a magic number (not in excluded list)
                    if num not in excluded and abs(num) not in excluded:
                        magic_numbers.append({
                            'line': line_num,
                            'number': num,
                            'context': line.strip()[:50],
                            'file': file_path
                        })
                except ValueError:
                    continue
        
        return magic_numbers
    
    def detect_feature_envy(self, tree: ast.AST, source_code: str, file_path: str) -> List[Dict]:
        """Detect feature envy - methods that access more external data than internal"""
        feature_envy_methods = []
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                external_access = 0
                internal_access = 0
                
                # Check if it's a method (has self parameter)
                is_method = (node.args.args and 
                           len(node.args.args) > 0 and 
                           node.args.args[0].arg in ('self', 'cls'))
                
                if not is_method:
                    continue  # Skip functions that aren't methods
                
                for item in ast.walk(node):
                    if isinstance(item, ast.Attribute):
                        # Check if accessing self.attribute (internal) or other.attribute (external)
                        if (isinstance(item.value, ast.Name) and 
                            item.value.id in ('self', 'cls')):
                            internal_access += 1
                        elif (isinstance(item.value, ast.Name) and 
                              item.value.id not in ('self', 'cls')):
                            external_access += 1
                
                # If more external access than internal, it might be feature envy
                if external_access > internal_access and external_access > 2:
                    feature_envy_methods.append({
                        'name': node.name,
                        'line': node.lineno,
                        'external_access': external_access,
                        'internal_access': internal_access,
                        'file': file_path
                    })
        
        return feature_envy_methods

def print_report(smells_found: Dict[str, List[Dict]], active_smells: List[str]) -> None:
    """Print a formatted report of detected smells"""
    print("\n" + "="*80)
    print("CODE SMELL DETECTION REPORT")
    print("="*80)
    print(f"Active smells evaluated: {', '.join(active_smells)}")
    print()
    
    total_smells = 0
    for smell_name, detections in smells_found.items():
        if detections and not isinstance(detections, dict):  # Skip error messages
            print(f"🔍 {smell_name}: {len(detections)} found")
            total_smells += len(detections)
            
            for detection in detections[:5]:  # Show first 5 detections per smell
                if smell_name == 'LongMethod':
                    print(f"   📍 {detection['name']} (lines {detection['line_range']}) - {detection['length']} lines")
                elif smell_name == 'GodClass':
                    print(f"   📍 {detection['name']} (lines {detection['line_range']}) - {detection['methods_count']} methods, {detection['attributes_count']} attributes")
                elif smell_name == 'DuplicatedCode':
                    print(f"   📍 Duplication: lines {detection['line_range_1']} ↔ {detection['line_range_2']}")
                elif smell_name == 'LargeParameterList':
                    print(f"   📍 {detection['name']} (line {detection['line']}) - {detection['parameter_count']} parameters")
                elif smell_name == 'MagicNumbers':
                    print(f"   📍 Line {detection['line']}: number {detection['number']} - '{detection['context']}'")
                elif smell_name == 'FeatureEnvy':
                    print(f"   📍 {detection['name']} (line {detection['line']}) - external: {detection['external_access']}, internal: {detection['internal_access']}")
            if len(detections) > 5:
                print(f"   ... and {len(detections) - 5} more")
            print()
    
    if total_smells == 0:
        print("✅ No code smells detected!")
    else:
        print(f"📊 Total smells found: {total_smells}")
    
    print("="*80)

def main():
    parser = argparse.ArgumentParser(description='Detect code smells in Python source files')
    parser.add_argument('files', nargs='+', help='Python source files to analyze')
    parser.add_argument('--config', '-c', default='config.yaml', help='Configuration file (default: config.yaml)')
    parser.add_argument('--only', help='Only run specific smells (comma-separated)')
    parser.add_argument('--exclude', help='Exclude specific smells (comma-separated)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Initialize detector
    detector = CodeSmellDetector()
    
    # Load configuration
    if os.path.exists(args.config):
        detector.load_config(args.config)
        if args.verbose:
            print(f"Loaded configuration from {args.config}")
    
    # Process CLI flags
    only_smells = args.only.split(',') if args.only else None
    exclude_smells = args.exclude.split(',') if args.exclude else None
    
    detector.update_config_from_cli(only_smells, exclude_smells)
    
    # Determine active smells
    active_smells = [smell for smell, config in detector.config.items() if config['enabled']]
    
    if args.verbose:
        print(f"Active smells: {', '.join(active_smells)}")
    
    # Analyze each file
    all_smells = {}
    for file_path in args.files:
        if not os.path.exists(file_path):
            print(f"Warning: File {file_path} not found, skipping...")
            continue
        
        if args.verbose:
            print(f"Analyzing {file_path}...")
        
        smells = detector.detect_smells(file_path)
        
        if 'error' in smells:
            print(f"Error analyzing {file_path}: {smells['error']}")
        else:
            all_smells[file_path] = smells
    
    # Print report for each file
    for file_path, smells in all_smells.items():
        print(f"\nFile: {file_path}")
        print_report(smells, active_smells)

if __name__ == '__main__':
    main()