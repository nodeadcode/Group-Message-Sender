from fastapi import FastAPI, Depends, HTTPException, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, timedelta
from pydantic import BaseModel
import jwt
import logging

# Local imports
from database import get_db, init_db
from models import User, Subscription, AccessCode, TelegramAccount, Campaign, AutoReplySettings
from config import (
    JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRATION_HOURS,
    PLANS, API_BASE_URL, WEBAPP_URL
)
from telegram_auth import verify_telegram_login
from telegram_auth import verify_telegram_login
# Removed telethon_login imports as they are used in auth.py now
from auto_reply import AutoReplyHandler
from auth import router as auth_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    version="1.0.0"
)

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for OTP sessions
otp_sessions = {}

# Request/Response Models
class TelegramAuthRequest(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str]
    username: Optional[str]
    photo_url: Optional[str]
    auth_date: int
    hash: str

class SendOTPRequest(BaseModel):
    api_id: int
    api_hash: str
    phone: str
    nickname: str

class VerifyOTPRequest(BaseModel):
    phone: str
    otp: str
    phone_code_hash: str
    session_string: str

class CreateCampaignRequest(BaseModel):
    account_id: int
    interval_minutes: int
    night_mode_enabled: bool
    groups: List[str]
    messages: List[str]

class UpdateCampaignRequest(BaseModel):
    interval_minutes: Optional[int]
    night_mode_enabled: Optional[bool]


class AutoReplySettingsUpdate(BaseModel):
    is_enabled: Optional[bool]
    reply_messages: Optional[List[str]]
    delay_seconds: Optional[int]
    use_random_message: Optional[bool]
    excluded_users: Optional[List[int]]

# Helper Functions
def create_jwt_token(user_id: int) -> str:
    """Create JWT token for authentication"""
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    """Dependency to get current authenticated user"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
    
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("user_id")
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def check_subscription(user_id: int, db: Session) -> dict:
    """Check if user has active subscription"""
    subscription = db.query(Subscription).filter(
        Subscription.user_id == user_id,
        Subscription.is_active == True,
        Subscription.expiry_date > datetime.utcnow()
    ).order_by(Subscription.expiry_date.desc()).first()
    
    if subscription:
        return {
            "has_access": True,
            "plan_type": subscription.plan_type,
            "expiry_date": subscription.expiry_date.isoformat(),
            "days_remaining": (subscription.expiry_date - datetime.utcnow()).days
        }
    
    return {
        "has_access": False,
        "plan_type": None,
        "expiry_date": None,
        "days_remaining": 0
    }

# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

@app.post("/auth/telegram")
async def telegram_auth(data: dict, db: Session = Depends(get_db)):
    """Authenticate user via Telegram Login Widget"""
    try:
        user_data = verify_telegram_login(data)
        
        # Get or create user
        user = db.query(User).filter(User.telegram_user_id == user_data["id"]).first()
        if not user:
            user = User(
                telegram_user_id=user_data["id"],
                username=user_data.get("username"),
                first_name=user_data.get("first_name"),
                last_name=user_data.get("last_name"),
                profile_photo_url=user_data.get("photo_url")
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
        # Create JWT token
        token = create_jwt_token(user.id)
        
        return {
            "status": "success",
            "token": token,
            "user": {
                "id": user.id,
                "telegram_user_id": user.telegram_user_id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "profile_photo_url": user.profile_photo_url
            }
        }
    except Exception as e:
        logger.error(f"Telegram auth error: {e}")
        raise HTTPException(status_code=403, detail=str(e))

# Mount Auth Router
app.include_router(auth_router)

# ============================================================================
# USER PROFILE ENDPOINTS
# ============================================================================

@app.get("/user/profile")
async def get_user_profile(user: User = Depends(get_current_user)):
    """Get current user's profile"""
    return {
        "id": user.id,
        "telegram_user_id": user.telegram_user_id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "bio": user.bio,
        "profile_photo_url": user.profile_photo_url,
        "is_owner": user.is_owner
    }

@app.put("/user/profile")
async def update_user_profile(bio: Optional[str] = None, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Update user profile"""
    if bio is not None:
        user.bio = bio
    db.commit()
    return {"status": "success"}

# ============================================================================
# SUBSCRIPTION ENDPOINTS
# ============================================================================

@app.get("/subscription/status")
async def get_subscription_status(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get user's subscription status"""
    return check_subscription(user.id, db)

@app.post("/subscription/validate")
async def validate_subscription(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Validate if user has active subscription"""
    status = check_subscription(user.id, db)
    if not status["has_access"]:
        raise HTTPException(status_code=403, detail="No active subscription")
    return status

# ============================================================================
# ACCOUNT MANAGEMENT ENDPOINTS
# ============================================================================

@app.get("/accounts")
async def list_accounts(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """List all Telegram accounts for user"""
    accounts = db.query(TelegramAccount).filter(TelegramAccount.user_id == user.id).all()
    return [{
        "id": acc.id,
        "nickname": acc.nickname,
        "phone": acc.phone,
        "is_active": acc.is_active,
        "status": acc.status,
        "last_used": acc.last_used.isoformat() if acc.last_used else None
    } for acc in accounts]

@app.delete("/accounts/{account_id}")
async def delete_account(account_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Delete a Telegram account"""
    account = db.query(TelegramAccount).filter(
        TelegramAccount.id == account_id,
        TelegramAccount.user_id == user.id
    ).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    db.delete(account)
    db.commit()
    return {"status": "success"}

@app.put("/accounts/{account_id}/activate")
async def activate_account(account_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Set account as active"""
    # Deactivate all accounts
    db.query(TelegramAccount).filter(TelegramAccount.user_id == user.id).update({"is_active": False})
    
    # Activate selected account
    account = db.query(TelegramAccount).filter(
        TelegramAccount.id == account_id,
        TelegramAccount.user_id == user.id
    ).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    account.is_active = True
    db.commit()
    return {"status": "success"}

@app.get("/accounts/{account_id}/status")
async def get_account_status(account_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Check account session status"""
    account = db.query(TelegramAccount).filter(
        TelegramAccount.id == account_id,
        TelegramAccount.user_id == user.id
    ).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    return {
        "status": account.status,
        "is_active": account.is_active,
        "last_used": account.last_used.isoformat() if account.last_used else None
    }

# ============================================================================
# CAMPAIGN ENDPOINTS
# ============================================================================

@app.post("/campaign/create")
async def create_campaign(request: CreateCampaignRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Create a new campaign"""
    # Validate subscription
    subscription = check_subscription(user.id, db)
    if not subscription["has_access"]:
        raise HTTPException(status_code=403, detail="No active subscription")
    
    campaign = Campaign(
        user_id=user.id,
        account_id=request.account_id,
        interval_minutes=request.interval_minutes,
        night_mode_enabled=request.night_mode_enabled,
        groups=request.groups,
        messages=request.messages,
        status="stopped"
    )
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    
    return {"status": "success", "campaign_id": campaign.id}

@app.post("/campaign/start")
async def start_campaign(campaign_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Start a campaign"""
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == user.id
    ).first()
    
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    campaign.status = "running"
    campaign.next_run = datetime.utcnow()
    db.commit()
    
    # TODO: Trigger scheduler
    
    return {"status": "success"}

@app.post("/campaign/stop")
async def stop_campaign(campaign_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Stop a campaign"""
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == user.id
    ).first()
    
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    campaign.status = "stopped"
    db.commit()
    
    return {"status": "success"}

@app.put("/campaign/update")
async def update_campaign(campaign_id: int, request: UpdateCampaignRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Update campaign settings"""
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == user.id
    ).first()
    
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    if request.interval_minutes is not None:
        campaign.interval_minutes = request.interval_minutes
    if request.night_mode_enabled is not None:
        campaign.night_mode_enabled = request.night_mode_enabled
    
    db.commit()
    return {"status": "success"}

@app.get("/campaign/status")
async def get_campaign_status(campaign_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get campaign status"""
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == user.id
    ).first()
    
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    return {
        "status": campaign.status,
        "last_run": campaign.last_run.isoformat() if campaign.last_run else None,
        "next_run": campaign.next_run.isoformat() if campaign.next_run else None,
        "interval_minutes": campaign.interval_minutes,
        "night_mode_enabled": campaign.night_mode_enabled
    }

# ============================================================================
# AUTO-REPLY ENDPOINTS
# ============================================================================

@app.get("/auto-reply/settings/{account_id}")
async def get_auto_reply_settings(account_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get auto-reply settings for account"""
    account = db.query(TelegramAccount).filter(
        TelegramAccount.id == account_id,
        TelegramAccount.user_id == user.id
    ).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    settings = db.query(AutoReplySettings).filter(AutoReplySettings.account_id == account_id).first()
    
    if not settings:
        return {
            "is_enabled": False,
            "reply_messages": [],
            "delay_seconds": 3,
            "use_random_message": False,
            "excluded_users": []
        }
    
    return {
        "is_enabled": settings.is_enabled,
        "reply_messages": settings.reply_messages,
        "delay_seconds": settings.delay_seconds,
        "use_random_message": settings.use_random_message,
        "excluded_users": settings.excluded_users
    }

@app.put("/auto-reply/settings/{account_id}")
async def update_auto_reply_settings(account_id: int, request: AutoReplySettingsUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Update auto-reply settings"""
    account = db.query(TelegramAccount).filter(
        TelegramAccount.id == account_id,
        TelegramAccount.user_id == user.id
    ).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    settings = db.query(AutoReplySettings).filter(AutoReplySettings.account_id == account_id).first()
    
    if not settings:
        settings = AutoReplySettings(
            account_id=account_id,
            is_enabled=False,
            reply_messages=["Thanks for your message!"],
            delay_seconds=3
        )
        db.add(settings)
    
    if request.is_enabled is not None:
        settings.is_enabled = request.is_enabled
    if request.reply_messages is not None:
        settings.reply_messages = request.reply_messages
    if request.delay_seconds is not None:
        settings.delay_seconds = request.delay_seconds
    if request.use_random_message is not None:
        settings.use_random_message = request.use_random_message
    if request.excluded_users is not None:
        settings.excluded_users = request.excluded_users
    
    db.commit()
    return {"status": "success"}

@app.post("/auto-reply/toggle/{account_id}")
async def toggle_auto_reply(account_id: int, enabled: bool, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Toggle auto-reply on/off"""
    settings = db.query(AutoReplySettings).filter(AutoReplySettings.account_id == account_id).first()
    
    if not settings:
        raise HTTPException(status_code=404, detail="Settings not found")
    
    settings.is_enabled = enabled
    db.commit()
    return {"status": "success"}

# ============================================================================
# STARTUP/SHUTDOWN
# ============================================================================

@app.on_event("startup")
async def startup():
    """Initialize database on startup"""
    logger.info("Initializing database...")
    init_db()
    logger.info("API started successfully!")

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "Spinify Ads API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }


# Admin / Owner Endpoints
@app.get("/api/admin/stats")
async def get_admin_stats(db: Session = Depends(get_db)):
    """Get platform-wide statistics (Owner only check in frontend/middleware ideally)"""
    # In a full impl, we'd check if request.user.id == OWNER_TELEGRAM_ID
    
    total_users = db.query(User).count()
    active_users = db.query(User).join(TelegramAccount).filter(TelegramAccount.is_active == True).distinct().count()
    active_automations = len(active_schedulers)
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "active_automations": active_automations,
        "total_messages_sent": 0 # Placeholder for now
    }

class BroadcastRequest(BaseModel):
    message: str

@app.post("/api/admin/broadcast")
async def broadcast_message(request: BroadcastRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Send broadcast to all users via Bot"""
    # Verify owner would happen here
    
    users = db.query(User).all()
    count = 0
    
    # Mock broadcast for now as we haven't set up the Bot Instance globally yet
    # In production: for user in users: bot.send_message(user.telegram_id, request.message)
    
    return {"status": "broadcast_queued", "recipient_count": len(users)}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
