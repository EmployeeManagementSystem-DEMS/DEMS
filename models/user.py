import bcrypt
from datetime import datetime

class User:
    def __init__(self, username, password, role="employee", emp_id=None):
        self.username = username
        self.password = self._hash_password(password)
        self.role = role
        self.emp_id = emp_id
        self.created_at = datetime.now()
    
    def _hash_password(self, password):
        """Hash password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password):
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "role": self.role,
            "emp_id": self.emp_id,
            "created_at": self.created_at
        }