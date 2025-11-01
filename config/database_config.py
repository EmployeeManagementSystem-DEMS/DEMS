import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConfig:
    # Single MongoDB URI for the cluster
    MONGO_URI = os.getenv('MONGO_URI')
    
    # Database names (3 databases in the same cluster)
    DB1_NAME = "ems_db1"
    DB2_NAME = "ems_db2"
    DB3_NAME = "ems_db3"
    
    # Employee ID ranges for horizontal fragmentation
    DB1_RANGE = (1, 1000)
    DB2_RANGE = (1001, 2000)
    DB3_RANGE = (2001, 3000)
    
    # Collection names
    EMPLOYEES_COLLECTION = "employees"
    DEPARTMENTS_COLLECTION = "departments"
    USERS_COLLECTION = "users"
    LEAVES_COLLECTION = "leaves"
    SALARIES_COLLECTION = "salaries"