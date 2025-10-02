#!/usr/bin/env python3
"""
Test the smell detector on our intentionally smelly code
"""

import subprocess
import sys

def test_detector():
    """Test the detector on the smelly code"""
    print("Testing Code Smell Detector on smell_code.py...")
    
    # Test with all smells enabled
    result = subprocess.run([
        sys.executable, 'smell_detector.py', 
        'smell_code.py',
        '--verbose'
    ], capture_output=True, text=True)
    
    print("STDOUT:")
    print(result.stdout)
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
    
    # Test with specific smells only
    print("\n" + "="*60)
    print("Testing with only LongMethod and MagicNumbers...")
    
    result2 = subprocess.run([
        sys.executable, 'smell_detector.py',
        'smell_code.py',
        '--only', 'LongMethod,MagicNumbers',
        '--verbose'
    ], capture_output=True, text=True)
    
    print("STDOUT:")
    print(result2.stdout)

if __name__ == '__main__':
    test_detector()