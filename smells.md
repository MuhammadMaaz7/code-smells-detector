import pypandoc

# The documentation text provided by the user
doc_text = """# Code Smells Documentation

## 1. Long Method
**File:** `smell_code.py`  
**Lines:** 10-85  

**Justification:**  
The `calculate_employee_compensation` method spans 75+ lines and handles multiple responsibilities including salary calculation, bonus computation, tax calculation, and data storage. This violates the Single Responsibility Principle.

---

## 2. God Class (Blob)
**File:** `smell_code.py`  
**Lines:** 1-175 (entire BusinessManager class)  

**Justification:**  
`BusinessManager` handles employee management, payroll processing, report generation, data validation, and bonus calculations - far too many unrelated responsibilities in one class.

---

## 3. Duplicated Code
**File:** `smell_code.py`  
**Lines:**  

- Tax calculation: 67-72 (in compensation) vs 126-131 (in report) vs 232-239 (standalone function)  
- Bonus calculation: 31-37 (in compensation) vs 108-114 (in report) vs 145-151 (in department bonuses)  

**Justification:**  
Identical tax and bonus calculation logic appears in multiple methods with slight variations, violating the DRY principle.

---

## 4. Large Parameter List
**File:** `smell_code.py`  
**Lines:**  

- 11-13: `calculate_employee_compensation` (10 parameters)  
- 89-91: `generate_payroll_report` (7 parameters)  
- 175-177: `validate_employee_data` (10 parameters)  

**Justification:**  
Multiple methods have 7-10 parameters, making them difficult to use and maintain. This suggests these parameters should be grouped into objects.

---

## 5. Magic Numbers
**File:** `smell_code.py`  
**Lines:** Throughout, but notably:  

- 16-22: `160, 1.5, 8.0, 2000, 1000, 500, 150`  
- 42-48: `1.15, 1.20, 1.05, 1.0` (department multipliers)  
- 67-72: `10000, 0.30, 7000, 0.25, 0.20` (tax brackets)  

**Justification:**  
Hard-coded numerical values appear throughout without named constants or configuration, making the code difficult to understand and maintain.

---

## 6. Feature Envy
**File:** `smell_code.py`  
**Lines:** 89-140 (`generate_payroll_report` method)  

**Justification:**  
The `generate_payroll_report` method is overly concerned with Employee data and duplicates business logic that properly belongs in the compensation calculation methods, accessing and manipulating data that should be encapsulated elsewhere.
"""