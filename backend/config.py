import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Application Settings
APP_NAME = "Spinify Ads"
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
WEBAPP_URL = os.getenv("WEBAPP_URL", "http://localhost:8080")

# Bot Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "8554290865:AAH1qQ0jOSkdj7A6LGCP1rm_KWvCgp_jaqs")
OWNER_TELEGRAM_ID = int(os.getenv("OWNER_TELEGRAM_ID", "0"))  # Set your Telegram ID

# Security
SESSION_SECRET = os.getenv("SESSION_SECRET", "CHANGE_THIS_SECRET_KEY_IN_PRODUCTION")
JWT_SECRET = os.getenv("JWT_SECRET", "CHANGE_THIS_JWT_SECRET_IN_PRODUCTION")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24 * 7  # 7 days

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# Subscription Plans
PLANS = {
    "weekly": {
        "price": 99,
        "duration_days": 7,
        "name": "Weekly Plan"
    },
    "monthly": {
        "price": 299,
        "duration_days": 30,
        "name": "Monthly Plan"
    }
}

# Campaign Settings
MIN_INTERVAL_MINUTES = 20
MAX_INTERVAL_MINUTES = 240  # 4 hours
GROUP_DELAY_SECONDS = 60
MESSAGE_DELAY_SECONDS = 60
NIGHT_MODE_START_HOUR = 0  # 12:00 AM
NIGHT_MODE_END_HOUR = 6    # 6:00 AM

# Auto-Reply Settings
AUTO_REPLY_MIN_DELAY = 2
AUTO_REPLY_MAX_DELAY = 5
