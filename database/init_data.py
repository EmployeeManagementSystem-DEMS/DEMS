from database.services import DatabaseService
from datetime import datetime

class DataInitializer:
    def __init__(self):
        self.db_service = DatabaseService()
    
    def initialize_system(self):
        """Initialize the system with default data"""
        print("🚀 Initializing DEMS with default data...")
        
        # Create default admin user
        self.create_default_admin()
        
        # Create default departments
        self.create_default_departments()
        
        # Create sample employees (optional)
        self.create_sample_employees()
        
        print("✅ System initialization completed!")
    
    def create_default_admin(self):
        """Create default admin user"""
        try:
            # Check if admin already exists
            existing_admin = self.db_service.authenticate_user("admin", "admin123")
            if existing_admin:
                print("ℹ️ Default admin already exists")
                return
            
            success = self.db_service.create_user("admin", "admin123", "admin")
            if success:
                print("✅ Default admin created (username: admin, password: admin123)")
            else:
                print("❌ Failed to create default admin")
        except Exception as e:
            print(f"❌ Error creating admin: {e}")
    
    def create_default_departments(self):
        """Create default departments"""
        departments = [
            ("HR", "Human Resources", "Manages employee relations and policies"),
            ("IT", "Information Technology", "Handles technology infrastructure and support"),
            ("FIN", "Finance", "Manages company finances and accounting"),
            ("MKT", "Marketing", "Handles marketing and promotional activities"),
            ("OPS", "Operations", "Manages day-to-day business operations")
        ]
        
        for dept_id, name, description in departments:
            try:
                success = self.db_service.create_department(dept_id, name, description)
                if success:
                    print(f"✅ Created department: {name}")
                else:
                    print(f"ℹ️ Department {name} already exists")
            except Exception as e:
                print(f"❌ Error creating department {name}: {e}")
    
    def create_sample_employees(self):
        """Create sample employees across all database fragments"""
        sample_employees = [
            # Database 1 (IDs 1-1000)
            # (emp_id, name, email, phone, date_of_birth, department, position, salary)
            (101, "Sifat Chowdhury", "sifat.c@company.com", "01571203416", "1990-05-15", "IT", "Software Developer", 75000),
            (205, "Sara Karim", "sara.k@company.com", "01832453216", "1988-08-22", "HR", "HR Manager", 85000),
            (350, "Bidhan Chandra", "bidhan.c@company.com", "01922853178", "1992-03-10", "FIN", "Accountant", 65000),
            
            # Database 2 (IDs 1001-2000)
            (1150, "Nafisa Atik", "nafisa.a@company.com", "01934084030", "2004-11-30", "MKT", "Marketing Specialist", 70000),
            (1300, "Rafiad Islam", "rafiad.i@company.com", "01772777388", "1985-07-18", "OPS", "Operations Manager", 90000),
            
            
            # Database 3 (IDs 2001-3000)
            (2100, "Asif Sarder", "asif.s@company.com", "01704400372", "1993-09-12", "FIN", "Financial Analyst", 72000),
            (2400, "Chironjeet Kabiraj", "chironjeet.k@company.com", "01584488392", "1994-01-05", "HR", "Recruiter", 60000),
        ]
        
        created_count = 0
        for emp_data in sample_employees:
            try:
                success, message = self.db_service.create_employee(*emp_data)
                if success:
                    created_count += 1
                    print(f"✅ Created employee {emp_data[1]} (ID: {emp_data[0]}, DOB: {emp_data[4]})")
                else:
                    print(f"ℹ️ Employee {emp_data[1]} already exists")
            except Exception as e:
                print(f"❌ Error creating employee {emp_data[1]}: {e}")
        
        print(f"✅ Created {created_count} sample employees")
    
    def get_database_for_employee(self, emp_id):
        """Helper to show which database an employee is stored in"""
        if 1 <= emp_id <= 1000:
            return "ems_db1"
        elif 1001 <= emp_id <= 2000:
            return "ems_db2"
        elif 2001 <= emp_id <= 3000:
            return "ems_db3"
        else:
            return "unknown"

if __name__ == "__main__":
    initializer = DataInitializer()
    initializer.initialize_system()