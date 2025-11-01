from datetime import datetime

class Leave:
    def __init__(self, emp_id, start_date, end_date, leave_type, reason):
        self.emp_id = int(emp_id)
        self.start_date = start_date
        self.end_date = end_date
        self.leave_type = leave_type
        self.reason = reason
        self.status = "Pending"
        self.applied_date = datetime.now()
        self.approved_by = None
        self.approved_date = None
    
    def to_dict(self):
        return {
            "emp_id": self.emp_id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "leave_type": self.leave_type,
            "reason": self.reason,
            "status": self.status,
            "applied_date": self.applied_date,
            "approved_by": self.approved_by,
            "approved_date": self.approved_date
        }