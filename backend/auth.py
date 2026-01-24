from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import os
import logging

# Import from parent package if possible, or use relative imports
# Depending on how the app is run (from root vs backend dir)
# We'll use the current working imports from main.py as a guide
try:
    from telethon_login import send_otp, verify_otp, verify_password
    from database import get_db
    from models import User, TelegramAccount
except ImportError:
    # If running from root package context
    from backend.telethon_login import send_otp, verify_otp, verify_password
    from backend.database import get_db
    from backend.models import User, TelegramAccount

router = APIRouter()
logger = logging.getLogger(__name__)

# In-memory storage for OTP sessions (moved from main.py)
# We need to share this or keep it in the router module
otp_sessions = {}

# =====================
# REQUEST MODELS
# =====================
class SendOTPRequest(BaseModel):
    api_id: int
    api_hash: str
    phone: str
    nickname: str = None  # Added nickname field as used in frontend

class VerifyOTPRequest(BaseModel):
    api_id: int = 0      # Optional if using session key
    api_hash: str = ""   # Optional if using session key
    phone: str
    otp: str
    phone_code_hash: str
    session_string: str

# =====================
# ROUTES
# =====================
@router.post("/auth/send-otp")
async def send_otp_route(request: SendOTPRequest):
    """Send OTP to phone number"""
    try:
        result = await send_otp(request.api_id, request.api_hash, request.phone)
        
        # Store session info with phone as temporary key
        session_key = f"temp_{request.phone}"
        otp_sessions[session_key] = {
            "phone_code_hash": result["phone_code_hash"],
            "session": result["session_string"],
            "api_id": request.api_id,
            "api_hash": request.api_hash,
            "nickname": request.nickname
        }
        
        return {
            "status": "success",
            "phone_code_hash": result["phone_code_hash"],
            "session_string": result["session_string"]
        }
    except Exception as e:
        logger.error(f"Send OTP error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/auth/verify-otp")
async def verify_otp_route(request: VerifyOTPRequest, db: Session = Depends(get_db)):
    """Verify OTP and authenticate user"""
    try:
        session_key = f"temp_{request.phone}"
        session_data = otp_sessions.get(session_key)
        
        if not session_data:
            raise HTTPException(status_code=400, detail="Session expired or invalid")
            
        # 1. Get or create internal User
        user = db.query(User).filter(User.telegram_user_id == 0).first()
        if not user:
            user = User(
                telegram_user_id=0, # Placeholder
                username=f"user_{request.phone.replace('+', '')}",
                first_name="User"
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            
        # 2. Verify with Telethon
        # Use session data if API credentials missing in request
        api_id = request.api_id if request.api_id else session_data["api_id"]
        api_hash = request.api_hash if request.api_hash else session_data["api_hash"]
        
        result = await verify_otp(
            api_id,
            api_hash,
            request.phone,
            request.otp,
            request.phone_code_hash,
            request.session_string
        )
        
        # 3. Save session file (required for bot)
        session_dir = "sessions"
        os.makedirs(session_dir, exist_ok=True)
        session_path = os.path.join(session_dir, f"{user.id}.session")
        
        with open(session_path, "w") as f:
            f.write(result["session"])
            
        # 4. Create/Update TelegramAccount
        # This part was in main.py, moving it here or ensuring main.py handles it
        # The user's snippet didn't include DB logic, but we MUST have it
        account = TelegramAccount(
            user_id=user.id,
            phone_number=request.phone,
            api_id=str(api_id),
            api_hash=api_hash,
            session_file=session_path,
            is_active=True
        )
        db.add(account)
        try:
            db.commit()
        except:
            db.rollback()
            # If account exists, update it
            existing = db.query(TelegramAccount).filter(
                TelegramAccount.phone_number == request.phone
            ).first()
            if existing:
                existing.session_file = session_path
                existing.is_active = True
                db.commit()

        return result
        
    except Exception as e:
        logger.error(f"Verify OTP error: {e}")
class VerifyPasswordRequest(BaseModel):
    phone: str
    password: str
    phone_code_hash: str
    session_string: str
    api_id: int = 0
    api_hash: str = ""


@router.post("/auth/2fa")
async def verify_password_route(request: VerifyPasswordRequest, db: Session = Depends(get_db)):
    """Verify 2FA password"""
    try:
        session_key = f"temp_{request.phone}"
        session_data = otp_sessions.get(session_key)
        
        if not session_data:
            raise HTTPException(status_code=400, detail="Session expired or invalid")
            
        # Get or create user
        user = db.query(User).filter(User.telegram_user_id == 0).first()
        if not user:
            user = User(
                telegram_user_id=0,
                username=f"user_{request.phone.replace('+', '')}",
                first_name="User"
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            
        # Verify Password
        api_id = request.api_id if request.api_id else session_data["api_id"]
        api_hash = request.api_hash if request.api_hash else session_data["api_hash"]
        
        result = await verify_password(
            api_id,
            api_hash,
            request.phone,
            request.password,
            request.phone_code_hash,
            request.session_string
        )
        
        # Save session
        session_dir = "sessions"
        os.makedirs(session_dir, exist_ok=True)
        session_path = os.path.join(session_dir, f"{user.id}.session")
        
        with open(session_path, "w") as f:
            f.write(result["session"])
            
        # Update Account
        account = TelegramAccount(
            user_id=user.id,
            phone_number=request.phone,
            api_id=str(api_id),
            api_hash=api_hash,
            session_file=session_path,
            is_active=True
        )
        db.add(account)
        try:
            db.commit()
        except:
            db.rollback()
            existing = db.query(TelegramAccount).filter(
                TelegramAccount.phone_number == request.phone
            ).first()
            if existing:
                existing.session_file = session_path
                existing.is_active = True
                db.commit()

        return result
        
    except Exception as e:
        logger.error(f"2FA Verify error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
