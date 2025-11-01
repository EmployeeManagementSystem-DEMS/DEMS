from datetime import datetime

class Employee:
    def __init__(self, emp_id, name, email, phone, department, position, salary, date_of_birth=None, join_date=None):
        self.emp_id = int(emp_id)
        self.name = name
        self.email = email
        self.phone = phone
        self.department = department
        self.position = position
        self.salary = float(salary)
        self.date_of_birth = date_of_birth
        self.join_date = join_date or datetime.now()
        self.status = "Active"
        self.created_at = datetime.now()
    
    def to_dict(self):
        return {
            "emp_id": self.emp_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "department": self.department,
            "position": self.position,
            "salary": self.salary,
            "date_of_birth": self.date_of_birth,
            "join_date": self.join_date,
            "status": self.status,
            "created_at": self.created_at
        }