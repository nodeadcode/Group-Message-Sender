from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os

# Database file path
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# SQLite optimizations to prevent locking
def _fk_pragma_on_connect(dbapi_con, con_record):
    """Enable foreign keys and set SQLite pragmas"""
    dbapi_con.execute('PRAGMA foreign_keys=ON')
    dbapi_con.execute('PRAGMA journal_mode=WAL')  # Write-Ahead Logging for better concurrency
    dbapi_con.execute('PRAGMA synchronous=NORMAL')  # Balance between safety and speed
    dbapi_con.execute('PRAGMA temp_store=MEMORY')  # Store temp tables in memory
    dbapi_con.execute('PRAGMA mmap_size=30000000000')  # Memory-mapped I/O
    dbapi_con.execute('PRAGMA page_size=4096')  # Optimal page size
    dbapi_con.execute('PRAGMA cache_size=10000')  # Larger cache

# Create engine with optimizations
if "sqlite" in DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        connect_args={
            "check_same_thread": False,  # Allow multiple threads
            "timeout": 30  # 30 second timeout to avoid lock errors
        },
        poolclass=StaticPool,  # Use static pool for SQLite
        echo=False  # Set to True for SQL debugging
    )
    event.listen(engine, "connect", _fk_pragma_on_connect)
else:
    # For PostgreSQL or other databases
    engine = create_engine(
        DATABASE_URL,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,  # Verify connections before using
        pool_recycle=3600,  # Recycle connections after 1 hour
        echo=False
    )

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False  # Prevent "object not bound" errors
)

# Base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    """Get database session with automatic cleanup"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database
def init_db():
    """Initialize database and create all tables"""
    # Import models here to avoid circular dependency
    from models import (
        User, Subscription, AccessCode, TelegramAccount, 
        Campaign, AutoReplySettings
    )
    Base.metadata.create_all(bind=engine)
