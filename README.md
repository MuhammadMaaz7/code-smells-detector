# Code Smell Detection Tool

A Python application that detects 6 common code smells in Python source code.

## Features

- **6 Code Smells Detected**:
  - Long Method
  - God Class (Blob)
  - Duplicated Code
  - Large Parameter List
  - Magic Numbers
  - Feature Envy

- **Flexible Configuration**:
  - YAML configuration file
  - CLI flag overrides
  - Enable/disable specific smells

## Usage

### Basic Usage

- **With Configuration**:
```bash
- python smell_detector.py --config my_config.yaml smell_code.py

- **Enable Only Specific Smells**:
```bash
- python smell_detector.py --only LongMethod,MagicNumbers smell_code.py

- **Exclude Specific Smells**:
```bash
- python smell_detector.py --exclude GodClass,DuplicatedCode smell_code.py

- **Verbose Output**:
```bash
- python smell_detector.py --verbose smell_code.py