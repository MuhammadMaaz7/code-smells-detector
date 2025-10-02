class BusinessManager:
    def __init__(self):
        self.employees = []
        self.projects = []
        self.departments = []
        self.financial_records = []
        self.performance_data = []
    
    def calculate_employee_compensation(self, employee_id, base_salary, hours_worked, overtime_hours, 
                                      performance_score, years_of_service, department_code, 
                                      location_multiplier, has_certification, project_completions):
        # Magic numbers scattered throughout
        STANDARD_HOURS = 160
        OVERTIME_RATE = 1.5
        BONUS_THRESHOLD = 8.0
        HIGH_PERFORMANCE_BONUS = 2000
        MEDIUM_PERFORMANCE_BONUS = 1000
        LOW_PERFORMANCE_BONUS = 500
        EXPERIENCE_BONUS_RATE = 150
        
        # Calculate base monthly salary
        monthly_salary = base_salary / 12
        
        # Overtime calculation (this logic gets duplicated later)
        hourly_rate = base_salary / (STANDARD_HOURS * 12)
        overtime_pay = overtime_hours * hourly_rate * OVERTIME_RATE
        
        # Performance bonus calculation
        if performance_score >= 9.0:
            performance_bonus = HIGH_PERFORMANCE_BONUS
        elif performance_score >= 7.5:
            performance_bonus = MEDIUM_PERFORMANCE_BONUS
        else:
            performance_bonus = LOW_PERFORMANCE_BONUS
        
        # Experience bonus
        experience_bonus = years_of_service * EXPERIENCE_BONUS_RATE
        
        # Department adjustment (magic numbers)
        if department_code == "ENG":
            dept_multiplier = 1.15
        elif department_code == "SALES":
            dept_multiplier = 1.20
        elif department_code == "HR":
            dept_multiplier = 1.05
        else:
            dept_multiplier = 1.0
        
        # Certification bonus
        certification_bonus = 500 if has_certification else 0
        
        # Project completion bonus
        project_bonus = project_completions * 300
        
        # Gross pay calculation
        gross_pay = (monthly_salary + overtime_pay) * dept_multiplier * location_multiplier
        total_bonus = performance_bonus + experience_bonus + certification_bonus + project_bonus
        
        # Tax calculation (duplicated logic - also exists in generate_payroll_report)
        if gross_pay + total_bonus > 10000:
            tax_rate = 0.30
        elif gross_pay + total_bonus > 7000:
            tax_rate = 0.25
        else:
            tax_rate = 0.20
        
        tax_amount = (gross_pay + total_bonus) * tax_rate
        net_pay = gross_pay + total_bonus - tax_amount
        
        # Update all class data (God Class - doing too much)
        employee_record = {
            'id': employee_id,
            'salary': base_salary,
            'gross_pay': gross_pay,
            'net_pay': net_pay,
            'department': department_code
        }
        self.employees.append(employee_record)
        
        financial_record = {
            'employee_id': employee_id,
            'tax_amount': tax_amount,
            'bonus_amount': total_bonus
        }
        self.financial_records.append(financial_record)
        
        performance_record = {
            'employee_id': employee_id,
            'performance_score': performance_score,
            'years_service': years_of_service
        }
        self.performance_data.append(performance_record)
        
        return net_pay, total_bonus, tax_amount

    def generate_payroll_report(self, employee_id, base_salary, hours_worked, overtime_hours,
                               performance_score, years_of_service, department_code):
        # This method duplicates compensation calculation logic (Code Smell: Duplicated Code)
        
        # Magic numbers (same as above but duplicated)
        STANDARD_HOURS = 160
        OVERTIME_RATE = 1.5
        BONUS_THRESHOLD = 8.0
        HIGH_PERFORMANCE_BONUS = 2000
        MEDIUM_PERFORMANCE_BONUS = 1000
        
        # Duplicated overtime calculation
        hourly_rate = base_salary / (STANDARD_HOURS * 12)
        overtime_pay = overtime_hours * hourly_rate * OVERTIME_RATE
        
        # Duplicated performance bonus logic
        if performance_score >= 9.0:
            performance_bonus = HIGH_PERFORMANCE_BONUS
        elif performance_score >= 7.5:
            performance_bonus = MEDIUM_PERFORMANCE_BONUS
        else:
            performance_bonus = 500  # Magic number instead of using constant
        
        # Duplicated department adjustment
        if department_code == "ENG":
            dept_multiplier = 1.15
        elif department_code == "SALES":
            dept_multiplier = 1.20
        else:
            dept_multiplier = 1.0
        
        monthly_salary = base_salary / 12
        gross_pay = (monthly_salary + overtime_pay) * dept_multiplier
        
        # Duplicated tax calculation
        if gross_pay + performance_bonus > 10000:
            tax_rate = 0.30
        elif gross_pay + performance_bonus > 7000:
            tax_rate = 0.25
        else:
            tax_rate = 0.20
        
        tax_amount = (gross_pay + performance_bonus) * tax_rate
        
        # Feature Envy - this method is too concerned with Employee data
        report = {
            'employee_id': employee_id,
            'gross_pay': round(gross_pay, 2),
            'overtime_pay': round(overtime_pay, 2),
            'performance_bonus': performance_bonus,
            'tax_amount': round(tax_amount, 2),
            'net_pay': round(gross_pay + performance_bonus - tax_amount, 2),
            'department': department_code
        }
        
        return report

    def process_department_bonuses(self, department_employees):
        # This method also contains duplicated bonus logic
        bonuses = []
        
        for emp in department_employees:
            # Magic numbers for bonus calculation
            if emp['performance_score'] >= 9.0:
                bonus = 2000
            elif emp['performance_score'] >= 7.5:
                bonus = 1000
            else:
                bonus = 500
            
            # Duplicated department multiplier logic
            if emp['department'] == "ENG":
                multiplier = 1.15
            elif emp['department'] == "SALES":
                multiplier = 1.20
            else:
                multiplier = 1.0
            
            final_bonus = bonus * multiplier
            bonuses.append({
                'employee_id': emp['id'],
                'bonus_amount': final_bonus
            })
        
        return bonuses

    def validate_employee_data(self, employee_id, base_salary, hours_worked, overtime_hours,
                             performance_score, years_of_service, department_code,
                             location_multiplier, has_certification, project_completions):
        # Large Parameter List again
        errors = []
        
        if base_salary < 30000 or base_salary > 200000:
            errors.append("Base salary out of range")
        
        if hours_worked < 0 or hours_worked > 300:
            errors.append("Invalid hours worked")
        
        if overtime_hours < 0 or overtime_hours > 100:
            errors.append("Invalid overtime hours")
        
        if performance_score < 0 or performance_score > 10:
            errors.append("Invalid performance score")
        
        # Magic numbers in validation
        if years_of_service < 0 or years_of_service > 50:
            errors.append("Invalid years of service")
        
        return errors

def calculate_tax_amount(gross_income, deductions=0):
    # Standalone function that duplicates tax logic (Duplicated Code)
    taxable_income = gross_income - deductions
    
    if taxable_income > 10000:  # Magic number
        tax_rate = 0.30
    elif taxable_income > 7000:  # Magic number
        tax_rate = 0.25
    else:
        tax_rate = 0.20  # Magic number
    
    return taxable_income * tax_rate

def main():
    manager = BusinessManager()
    
    # Test the system
    net_pay, total_bonus, tax_amount = manager.calculate_employee_compensation(
        employee_id=101,
        base_salary=75000,
        hours_worked=160,
        overtime_hours=15,
        performance_score=8.7,
        years_of_service=5,
        department_code="ENG",
        location_multiplier=1.1,
        has_certification=True,
        project_completions=3
    )
    
    print(f"Employee Compensation Results:")
    print(f"Net Pay: ${net_pay:.2f}")
    print(f"Total Bonus: ${total_bonus:.2f}")
    print(f"Tax Amount: ${tax_amount:.2f}")
    
    # Generate report (duplicates calculations)
    report = manager.generate_payroll_report(
        employee_id=101,
        base_salary=75000,
        hours_worked=160,
        overtime_hours=15,
        performance_score=8.7,
        years_of_service=5,
        department_code="ENG"
    )
    
    print(f"\nPayroll Report:")
    print(f"Gross Pay: ${report['gross_pay']}")
    print(f"Net Pay: ${report['net_pay']}")
    
    # Validate data
    errors = manager.validate_employee_data(
        employee_id=101,
        base_salary=75000,
        hours_worked=160,
        overtime_hours=15,
        performance_score=8.7,
        years_of_service=5,
        department_code="ENG",
        location_multiplier=1.1,
        has_certification=True,
        project_completions=3
    )
    
    if errors:
        print(f"\nValidation Errors: {errors}")
    else:
        print("\nData validation passed")

if __name__ == "__main__":
    main()