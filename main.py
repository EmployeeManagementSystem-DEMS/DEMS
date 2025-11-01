#!/usr/bin/env python3
"""
Employee Management System (EMS)
Main application entry point
"""

import sys
import os
from database.init_data import DataInitializer
from gui.login_window import LoginWindow

def main():
    """Main application function"""
    print("🚀 Starting Employee Management System (EMS)")
    print("=" * 50)
    
    try:
        # Initialize system with default data
        print("📊 Initializing system...")
        initializer = DataInitializer()
        initializer.initialize_system()
        
        print("\n" + "=" * 50)
        print("🖥️  Starting GUI Application...")
        print("Default Admin Login:")
        print("Username: admin")
        print("Password: admin123")
        print("=" * 50)
        
        # Start GUI application
        app = LoginWindow()
        app.run()
        
    except KeyboardInterrupt:
        print("\n👋 Application terminated by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()