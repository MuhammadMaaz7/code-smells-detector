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
```bash
python smell_detector.py file1.py file2.py