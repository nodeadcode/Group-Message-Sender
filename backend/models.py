from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_user_id = Column(Integer, unique=True, nullable=False, index=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    profile_photo_url = Column(String, nullable=True)
    is_owner = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    subscriptions = relationship("Subscription", back_populates="user")
    telegram_accounts = relationship("TelegramAccount", back_populates="user")
    campaigns = relationship("Campaign", back_populates="user")

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan_type = Column(String, nullable=False)  # weekly or monthly
    price = Column(Integer, nullable=False)  # 99 or 299
    start_date = Column(DateTime, default=datetime.utcnow)
    expiry_date = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="subscriptions")

class AccessCode(Base):
    __tablename__ = "access_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False, index=True)
    plan_type = Column(String, nullable=False)  # weekly or monthly
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    used_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    is_used = Column(Boolean, default=False)
    used_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class TelegramAccount(Base):
    __tablename__ = "telegram_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    nickname = Column(String, nullable=False)
    api_id = Column(Integer, nullable=False)
    api_hash = Column(String, nullable=False)  # Should be encrypted
    phone = Column(String, nullable=False)
    session_file = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    status = Column(String, default="pending")  # authenticated/expired/pending
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="telegram_accounts")
    campaigns = relationship("Campaign", back_populates="account")
    auto_reply_settings = relationship("AutoReplySettings", back_populates="account", uselist=False)

class Campaign(Base):
    __tablename__ = "campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    account_id = Column(Integer, ForeignKey("telegram_accounts.id"), nullable=False)
    interval_minutes = Column(Integer, default=60)
    night_mode_enabled = Column(Boolean, default=False)
    groups = Column(JSON, nullable=False)  # list of group links
    messages = Column(JSON, nullable=False)  # list of messages
    status = Column(String, default="stopped")  # running/stopped/paused
    last_run = Column(DateTime, nullable=True)
    next_run = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="campaigns")
    account = relationship("TelegramAccount", back_populates="campaigns")

class AutoReplySettings(Base):
    __tablename__ = "auto_reply_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("telegram_accounts.id"), nullable=False, unique=True)
    is_enabled = Column(Boolean, default=False)
    reply_messages = Column(JSON, nullable=False)  # list of reply templates
    delay_seconds = Column(Integer, default=3)  # 2-5 seconds
    use_random_message = Column(Boolean, default=False)
    excluded_users = Column(JSON, default=[])  # list of user IDs to exclude
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    account = relationship("TelegramAccount", back_populates="auto_reply_settings")
