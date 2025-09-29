from smelly_code2 import BusinessManager, calculate_tax_amount

def test_basic_compensation():
    """Simple test for basic compensation calculation"""
    print("=== Testing Basic Compensation ===")
    manager = BusinessManager()
    
    net_pay, total_bonus, tax_amount = manager.calculate_employee_compensation(
        employee_id=1,
        base_salary=60000,
        hours_worked=160,
        overtime_hours=10,
        performance_score=8.0,
        years_of_service=3,
        department_code="HR",
        location_multiplier=1.0,
        has_certification=False,
        project_completions=2
    )
    
    print(f"Net Pay: ${net_pay:.2f}")
    print(f"Total Bonus: ${total_bonus:.2f}")
    print(f"Tax Amount: ${tax_amount:.2f}")
    
    # Basic assertions
    assert net_pay > 0, "Net pay should be positive"
    assert total_bonus > 0, "Bonus should be positive"
    assert tax_amount > 0, "Tax amount should be positive"
    print("✓ Basic compensation test passed!\n")

def test_high_performer():
    """Test for high performing employee"""
    print("=== Testing High Performer ===")
    manager = BusinessManager()
    
    net_pay, total_bonus, tax_amount = manager.calculate_employee_compensation(
        employee_id=2,
        base_salary=100000,
        hours_worked=160,
        overtime_hours=5,
        performance_score=9.5,
        years_of_service=8,
        department_code="ENG",
        location_multiplier=1.1,
        has_certification=True,
        project_completions=5
    )
    
    print(f"High Performer Net Pay: ${net_pay:.2f}")
    print(f"High Performer Bonus: ${total_bonus:.2f}")
    
    assert total_bonus >= 2000, "High performer should get good bonus"
    assert net_pay > 6000, "High performer should have good net pay"
    print("✓ High performer test passed!\n")

def test_payroll_report():
    """Test payroll report generation"""
    print("=== Testing Payroll Report ===")
    manager = BusinessManager()
    
    report = manager.generate_payroll_report(
        employee_id=3,
        base_salary=50000,
        hours_worked=160,
        overtime_hours=8,
        performance_score=7.6,
        years_of_service=2,
        department_code="SALES"
    )
    
    print(f"Report: {report}")
    
    # Check required fields exist
    required_fields = ['employee_id', 'gross_pay', 'net_pay', 'department']
    for field in required_fields:
        assert field in report, f"Report should have {field}"
    
    assert report['employee_id'] == 3
    assert report['department'] == "SALES"
    print("✓ Payroll report test passed!\n")

def test_validation():
    """Test data validation"""
    print("=== Testing Data Validation ===")
    manager = BusinessManager()
    
    # Test valid data
    errors = manager.validate_employee_data(
        employee_id=4,
        base_salary=75000,
        hours_worked=160,
        overtime_hours=20,
        performance_score=8.5,
        years_of_service=10,
        department_code="ENG",
        location_multiplier=1.2,
        has_certification=True,
        project_completions=4
    )
    
    print(f"Valid data errors: {errors}")
    assert len(errors) == 0, "Valid data should have no errors"
    
    # Test invalid data
    errors = manager.validate_employee_data(
        employee_id=5,
        base_salary=25000,  # Too low
        hours_worked=400,   # Too high
        overtime_hours=-5,  # Negative
        performance_score=11, # Out of range
        years_of_service=60, # Too high
        department_code="IT",
        location_multiplier=0.8,
        has_certification=False,
        project_completions=2
    )
    
    print(f"Invalid data errors: {errors}")
    assert len(errors) > 0, "Invalid data should have errors"
    print("✓ Validation test passed!\n")

def test_department_bonuses():
    """Test department bonus calculation"""
    print("=== Testing Department Bonuses ===")
    manager = BusinessManager()
    
    employees = [
        {'id': 101, 'performance_score': 9.2, 'department': 'ENG'},
        {'id': 102, 'performance_score': 7.8, 'department': 'SALES'},
        {'id': 103, 'performance_score': 6.5, 'department': 'HR'}
    ]
    
    bonuses = manager.process_department_bonuses(employees)
    
    print(f"Bonuses: {bonuses}")
    
    assert len(bonuses) == 3, "Should return bonuses for all employees"
    
    for bonus in bonuses:
        assert 'employee_id' in bonus
        assert 'bonus_amount' in bonus
        assert bonus['bonus_amount'] > 0
    
    print("✓ Department bonuses test passed!\n")

def test_tax_calculation():
    """Test standalone tax calculation"""
    print("=== Testing Tax Calculation ===")
    
    tax1 = calculate_tax_amount(12000, 1000)  # High income
    tax2 = calculate_tax_amount(8000, 500)   # Medium income  
    tax3 = calculate_tax_amount(4000, 200)   # Low income
    
    print(f"High income tax: ${tax1:.2f}")
    print(f"Medium income tax: ${tax2:.2f}")
    print(f"Low income tax: ${tax3:.2f}")
    
    assert tax1 > 0 and tax2 > 0 and tax3 > 0
    assert tax1 > tax2 > tax3, "Higher income should pay more tax"
    print("✓ Tax calculation test passed!\n")

def test_data_storage():
    """Test that data is stored correctly"""
    print("=== Testing Data Storage ===")
    manager = BusinessManager()
    
    initial_count = len(manager.employees)
    
    manager.calculate_employee_compensation(
        employee_id=999,
        base_salary=80000,
        hours_worked=160,
        overtime_hours=12,
        performance_score=8.8,
        years_of_service=6,
        department_code="ENG",
        location_multiplier=1.1,
        has_certification=True,
        project_completions=3
    )
    
    print(f"Employees before: {initial_count}, after: {len(manager.employees)}")
    print(f"Financial records: {len(manager.financial_records)}")
    print(f"Performance data: {len(manager.performance_data)}")
    
    assert len(manager.employees) == initial_count + 1
    assert len(manager.financial_records) == initial_count + 1
    assert len(manager.performance_data) == initial_count + 1
    print("✓ Data storage test passed!\n")

def run_all_tests():
    """Run all test functions"""
    print("🧪 RUNNING ALL TESTS...\n")
    
    test_basic_compensation()
    test_high_performer()
    test_payroll_report()
    test_validation()
    test_department_bonuses()
    test_tax_calculation()
    test_data_storage()
    
    print("🎉 ALL TESTS PASSED! ✅")
    print("Note: The code has intentional smells but the functionality works correctly.")

if __name__ == "__main__":
    run_all_tests()