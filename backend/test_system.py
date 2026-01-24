#!/usr/bin/env python3
"""
Quick test script to verify all components are working
"""
import sys
import asyncio
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from models import User, TelegramAccount, Subscription, AccessCode
from config import BOT_TOKEN, OWNER_TELEGRAM_ID, PLANS, DATABASE_URL

def test_database():
    """Test database connection"""
    print("📊 Testing Database Connection...")
    try:
        db = SessionLocal()
        # Try a simple query
        user_count = db.query(User).count()
        print(f"   ✅ Database connected! ({user_count} users)")
        db.close()
        return True
    except Exception as e:
        print(f"   ❌ Database error: {e}")
        return False

def test_config():
    """Test configuration"""
    print("\n⚙️  Testing Configuration...")
    issues = []
    
    if not BOT_TOKEN or BOT_TOKEN == "your_bot_token_here":
        issues.append("BOT_TOKEN not set in .env")
    else:
        print(f"   ✅ BOT_TOKEN: {BOT_TOKEN[:20]}...")
    
    if OWNER_TELEGRAM_ID == 0:
        issues.append("OWNER_TELEGRAM_ID not set (find your ID with @userinfobot)")
    else:
        print(f"   ✅ OWNER_TELEGRAM_ID: {OWNER_TELEGRAM_ID}")
    
    print(f"   ✅ DATABASE_URL: {DATABASE_URL}")
    print(f"   ✅ Plans configured: {', '.join(PLANS.keys())}")
    
    if issues:
        print("\n   ⚠️  Configuration warnings:")
        for issue in issues:
            print(f"      • {issue}")
        return False
    return True

def test_models():
    """Test models can be created"""
    print("\n🏗️  Testing Models...")
    try:
        db = SessionLocal()
        
        # Test creating a user
        test_user = User(
            telegram_user_id=999999999,
            first_name="Test",
            username="testuser"
        )
        db.add(test_user)
        db.commit()
        
        # Clean up
        db.delete(test_user)
        db.commit()
        db.close()
        
        print("   ✅ All models working!")
        return True
    except Exception as e:
        print(f"   ❌ Model error: {e}")
        return False

async def test_imports():
    """Test all imports work"""
    print("\n📦 Testing Imports...")
    try:
        from telethon_login import send_otp, verify_otp
        print("   ✅ telethon_login")
        from telegram_auth import verify_telegram_login
        print("   ✅ telegram_auth")
        from auto_reply import AutoReplyHandler
        print("   ✅ auto_reply")
        return True
    except Exception as e:
        print(f"   ❌ Import error: {e}")
        return False

def main():
    print("🧪 Spinify Ads - System Test")
    print("=" * 60)
    
    results = {
        "Database": test_database(),
        "Configuration": test_config(),
        "Models": test_models(),
        "Imports": asyncio.run(test_imports())
    }
    
    print("\n" + "=" * 60)
    print("📋 Test Results:")
    
    all_passed = True
    for test, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {test}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 All tests passed! System is ready to use!")
        print("\n📝 Next steps:")
        print("   1. Start bot: cd bot && python bot.py")
        print("   2. Start backend: cd backend && uvicorn main:app --reload")
        print("   3. Start frontend: python -m http.server 8080 --directory webapp")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
