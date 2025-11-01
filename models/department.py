from datetime import datetime

class Department:
    def __init__(self, dept_id, name, description, manager=None):
        self.dept_id = dept_id
        self.name = name
        self.description = description
        self.manager = manager
        self.created_at = datetime.now()
    
    def to_dict(self):
        return {
            "dept_id": self.dept_id,
            "name": self.name,
            "description": self.description,
            "manager": self.manager,
            "created_at": self.created_at
        }