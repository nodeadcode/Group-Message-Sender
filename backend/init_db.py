#!/usr/bin/env python3
"""
Database initialization script
Run this before starting the backend for the first time
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import init_db, engine
from models import Base
from sqlalchemy import inspect

def main():
    print("🗄️  Initializing Spinify Ads Database...")
    print("-" * 50)
    
    try:
        # Initialize database
        init_db()
        
        # Verify tables created
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        print(f"\n✅ Database initialized successfully!")
        print(f"\n📊 Created {len(tables)} tables:")
        for table in tables:
            print(f"   • {table}")
        
        print("\n" + "-" * 50)
        print("✨ Database is ready to use!")
        print("\nNext steps:")
        print("  1. Update .env with your credentials")
        print("  2. Run: cd backend && uvicorn main:app --reload")
        print("  3. Visit: http://localhost:8000/docs")
        
    except Exception as e:
        print(f"\n❌ Error initializing database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
