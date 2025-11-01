from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from config.database_config import DatabaseConfig
import logging

class DatabaseManager:
    def __init__(self):
        self.client = None
        self.databases = {}
        self._connect_to_cluster()
    
    def _connect_to_cluster(self):
        """Connect to MongoDB Atlas cluster and access multiple databases"""
        try:
            # Single client connection to the cluster
            self.client = MongoClient(
                DatabaseConfig.MONGO_URI,
                serverSelectionTimeoutMS=5000
            )
            
            # Access different databases within the same cluster
            self.databases['db1'] = self.client[DatabaseConfig.DB1_NAME]
            self.databases['db2'] = self.client[DatabaseConfig.DB2_NAME]
            self.databases['db3'] = self.client[DatabaseConfig.DB3_NAME]
            
            # Test connection
            self.client.admin.command('ping')
            print("✅ Connected to MongoDB Atlas cluster")
            print(f"✅ Database 1: {DatabaseConfig.DB1_NAME}")
            print(f"✅ Database 2: {DatabaseConfig.DB2_NAME}")
            print(f"✅ Database 3: {DatabaseConfig.DB3_NAME}")
                
        except Exception as e:
            print(f"❌ Database connection error: {e}")
            raise
    
    def get_database_for_employee(self, emp_id):
        """Determine which database to use based on employee ID (Range Fragmentation)"""
        emp_id = int(emp_id)
        if DatabaseConfig.DB1_RANGE[0] <= emp_id <= DatabaseConfig.DB1_RANGE[1]:
            return self.databases['db1']
        elif DatabaseConfig.DB2_RANGE[0] <= emp_id <= DatabaseConfig.DB2_RANGE[1]:
            return self.databases['db2']
        elif DatabaseConfig.DB3_RANGE[0] <= emp_id <= DatabaseConfig.DB3_RANGE[1]:
            return self.databases['db3']
        else:
            raise ValueError(f"Employee ID {emp_id} is out of range (1-3000)!")
    
    def get_all_databases(self):
        """Get all databases for operations that need to query all fragments"""
        return list(self.databases.values())
    
    def get_database_info(self):
        """Get information about which database an employee ID would use"""
        return {
            'db1': f"Employee IDs {DatabaseConfig.DB1_RANGE[0]}-{DatabaseConfig.DB1_RANGE[1]}",
            'db2': f"Employee IDs {DatabaseConfig.DB2_RANGE[0]}-{DatabaseConfig.DB2_RANGE[1]}",
            'db3': f"Employee IDs {DatabaseConfig.DB3_RANGE[0]}-{DatabaseConfig.DB3_RANGE[1]}"
        }
    
    def close_connection(self):
        """Close database connection"""
        if self.client:
            self.client.close()