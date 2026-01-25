#!/usr/bin/env python3
"""
Spinify Ads - Telegram Bot
"""

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)
from telegram.constants import ParseMode
import random
import string
from datetime import datetime, timedelta
import sys
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from database import SessionLocal
from models import User, AccessCode, Subscription, TelegramAccount, Campaign
from config import PLANS, WEBAPP_URL

# Get credentials from environment
BOT_TOKEN = os.getenv('BOT_TOKEN')
OWNER_TELEGRAM_ID = int(os.getenv('OWNER_TELEGRAM_ID', 0))

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# =====================
# UTILITY FUNCTIONS
# =====================

def generate_code(length=10):
    """Generate a random access code"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def format_datetime(dt):
    """Format datetime for display"""
    if not dt:
        return "Never"
    return dt.strftime('%d %b %Y, %I:%M %p')


def get_user_stats(db, user_id):
    """Get user statistics"""
    user = db.query(User).filter(User.telegram_user_id == user_id).first()
    if not user:
        return None
    
    accounts = db.query(TelegramAccount).filter(
        TelegramAccount.user_id == user.id
    ).count()
    
    campaigns = db.query(Campaign).filter(
        Campaign.user_id == user.id
    ).count()
    
    subscription = db.query(Subscription).filter(
        Subscription.user_id == user.id,
        Subscription.is_active == True
    ).first()
    
    return {
        "accounts": accounts,
        "campaigns": campaigns,
        "subscription": subscription
    }


# =====================
# COMMAND HANDLERS
# =====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Premium card-style welcome with user profile"""
    user = update.message.from_user
    user_id = user.id
    
    db = SessionLocal()
    
    try:
        # Get user from database
        db_user = db.query(User).filter(User.telegram_user_id == user_id).first()
        
        # Get subscription info
        subscription = None
        if db_user:
            subscription = db.query(Subscription).filter(
                Subscription.user_id == db_user.id,
                Subscription.is_active == True
            ).first()
        
        # Build profile info
        username = f"@{user.username}" if user.username else "Guest"
        first_name = user.first_name or "User"
        is_premium = user.is_premium if hasattr(user, 'is_premium') else False
        premium_badge = "👑 PREMIUM" if is_premium else "STANDARD"
        
        # Subscription status
        if subscription:
            sub_badge = "✅ ACTIVE"
            sub_plan = subscription.plan_type.upper()
            days_left = (subscription.expiry_date - datetime.utcnow()).days
            if days_left < 0:
                days_left = 0
        else:
            sub_badge = "⚠️ INACTIVE"
            sub_plan = "FREE"
            days_left = 0
        
        keyboard = [
            [
                InlineKeyboardButton(
                    "🚀 Open Dashboard",
                    web_app=WebAppInfo(url=WEBAPP_URL)
                )
            ],
            [
                InlineKeyboardButton("👤 Profile", callback_data="cmd_profile"),
                InlineKeyboardButton("📊 Status", callback_data="my_status")
            ],
            [
                InlineKeyboardButton("⚙️ Settings", callback_data="campaign_settings"),
                InlineKeyboardButton("💳 Plans", callback_data="view_plans")
            ],
            [
                InlineKeyboardButton("📖 Help", callback_data="help"),
                InlineKeyboardButton("ℹ️ About", callback_data="about")
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Telegram profile-style welcome
        welcome_message = f"""
          🎭
     ━━━━━━━━━━━━━━

**{first_name}**
{username}

┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ **Profile**                      
┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛

ID: `{user_id}`
Tier: {premium_badge}

💳 **Subscription**
Plan: {sub_plan} {sub_badge}
Days Left: **{days_left}** days

━━━━━━━━━━━━━━━━━━━━━━━━━━

**🌟 SPINIFY ADS**
Premium Ad Automation

▤ Multi-Account Management
▤ Smart Scheduling (20-240min)
▤ Night Mode (10PM-6AM)
▤ Auto-Reply System
▤ Bulk Posting (10 groups)
▤ Secure OTP & 2FA

**💰 Plans**
▤ Weekly: ₹99 (7 days)
▤ Monthly: ₹299 (30 days) ⭐

━━━━━━━━━━━━━━━━━━━━━━━━━━
💻 @spinify
"""
        
        await update.message.reply_text(
            welcome_message,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
    finally:
        db.close()


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help message with all commands"""
    user_id = update.message.from_user.id
    is_owner = (user_id == OWNER_TELEGRAM_ID)
    
    help_text = """
📖 **COMMAND REFERENCE**
━━━━━━━━━━━━━━━━━━━

**👤 USER COMMANDS:**
▤ `/start` - Show welcome menu
▤ `/help` - Display this help
▤ `/status` - View your statistics
▤ `/settings` - Campaign configuration
▤ `/profile` - Show your Telegram profile
▤ `/redeem <code>` - Activate subscription
"""
    
    if is_owner:
        help_text += """
**👑 OWNER COMMANDS:**
▤ `/generate weekly` - Generate weekly code
▤ `/generate monthly` - Generate monthly code
▤ `/stats` - View global bot statistics
▤ `/broadcast <msg>` - Send message to all users
"""
    else:
        help_text += """
**👑 OWNER COMMANDS:**
▤ `/generate weekly` - Generate weekly code
▤ `/generate monthly` - Generate monthly code
"""
    
    help_text += """
**⚙️ CAMPAIGN SETTINGS:**
▤ Change intervals (min: 20 minutes)
▤ Adjust delays (min: 60 seconds)
▤ Set group gap (min: 60 seconds)
▤ Toggle night mode (10PM-6AM)
▤ Manage groups

**💡 TIPS:**
━━━━━━━━━━━━━━━━━━━
▤ Get API credentials from my.telegram.org
▤ Keep your session secure
▤ Use night mode to avoid spam detection
▤ Contact @spinify for support

**📱 DASHBOARD:**
Click "Open Dashboard" to access the full web interface for campaign management.

━━━━━━━━━━━━━━━━━━━
Need help? Contact @spinify
"""
    
    keyboard = [[InlineKeyboardButton("« Back to Start", callback_data="back_to_start")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        help_text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user status and statistics"""
    user_id = update.message.from_user.id
    db = SessionLocal()
    
    try:
        stats = get_user_stats(db, user_id)
        
        if not stats:
            await update.message.reply_text(
                "❌ **No account found!**\n\n"
                "Please use /start to initialize your account."
            )
            return
        
        sub = stats["subscription"]
        sub_status = "✅ Active" if sub else "❌ Inactive"
        sub_plan = sub.plan_type.upper() if sub else "None"
        sub_expiry = format_datetime(sub.expiry_date) if sub else "N/A"
        
        if sub and sub.expiry_date:
            days_left = (sub.expiry_date - datetime.utcnow()).days
            if days_left < 0:
                days_left = 0
        else:
            days_left = 0
        
        status_message = f"""
📊 **YOUR STATUS**
━━━━━━━━━━━━━━━━━━━

**👤 Account Info:**
▤ Status: {sub_status}
▤ Plan: {sub_plan}
▤ Days Left: {days_left}
▤ Expires: {sub_expiry}

**📱 Resources:**
▤ Telegram Accounts: {stats["accounts"]}
▤ Campaigns: {stats["campaigns"]}

**🔗 Quick Actions:**
"""
        
        keyboard = [
            [InlineKeyboardButton("🚀 Open Dashboard", web_app=WebAppInfo(url=WEBAPP_URL))],
            [InlineKeyboardButton("💳 View Plans", callback_data="view_plans")]
        ]
        
        if not sub or days_left <= 0:
            status_message += "\n⚠️ **Subscription expired or inactive!**\nUse `/redeem <code>` to activate."
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            status_message,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
    finally:
        db.close()


async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show campaign settings menu"""
    user_id = update.message.from_user.id
    db = SessionLocal()
    
    try:
        user = db.query(User).filter(User.telegram_user_id == user_id).first()
        
        if not user:
            await update.message.reply_text(
                "❌ **No account found!**\n\n"
                "Please use /start first."
            )
            return
        
        # Get active campaign settings
        campaign = db.query(Campaign).filter(
            Campaign.user_id == user.id
        ).first()
        
        if campaign:
            interval = campaign.interval_minutes
            night_mode = "✅ ON" if campaign.night_mode_enabled else "❌ OFF"
            groups_count = len(campaign.groups) if campaign.groups else 0
        else:
            interval = 60
            night_mode = "❌ OFF"
            groups_count = 0
        
        settings_text = f"""
⚙️ **CAMPAIGN SETTINGS**
━━━━━━━━━━━━━━━━━━━

**📊 Current Configuration:**
▤ Interval: {interval} minutes
▤ Message Delay: 60 seconds
▤ Group Gap: 60 seconds
▤ Night Mode: {night_mode}
▤ Groups: {groups_count}

**🔧 Available Settings:**
Use buttons below to configure:
"""
        
        keyboard = [
            [InlineKeyboardButton("⏰ Change Interval", callback_data="set_interval")],
            [InlineKeyboardButton("⏱️ Change Delays", callback_data="set_delays")],
            [InlineKeyboardButton("🌙 Toggle Night Mode", callback_data="toggle_night_mode")],
            [InlineKeyboardButton("👥 Manage Groups", callback_data="manage_groups")],
            [InlineKeyboardButton("« Back", callback_data="back_to_start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            settings_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
    finally:
        db.close()


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show global bot statistics - Owner only"""
    user_id = update.message.from_user.id
    
    if user_id != OWNER_TELEGRAM_ID:
        await update.message.reply_text(
            "🔒 **Access Denied**\n\n"
            "This command is restricted to the owner only."
        )
        return
    
    db = SessionLocal()
    
    try:
        # Get statistics
        total_users = db.query(User).count()
        total_accounts = db.query(TelegramAccount).count()
        total_campaigns = db.query(Campaign).count()
        active_campaigns = db.query(Campaign).filter(Campaign.status == "running").count()
        
        # Subscription stats
        active_subs = db.query(Subscription).filter(
            Subscription.is_active == True,
            Subscription.expiry_date > datetime.utcnow()
        ).count()
        
        weekly_subs = db.query(Subscription).filter(
            Subscription.plan_type == "weekly",
            Subscription.is_active == True
        ).count()
        
        monthly_subs = db.query(Subscription).filter(
            Subscription.plan_type == "monthly",
            Subscription.is_active == True
        ).count()
        
        # Access codes
        total_codes = db.query(AccessCode).count()
        used_codes = db.query(AccessCode).filter(AccessCode.is_used == True).count()
        unused_codes = total_codes - used_codes
        
        stats_text = f"""
📊 **BOT STATISTICS**
━━━━━━━━━━━━━━━━━━━

**👥 USERS:**
▤ Total Users: {total_users}
▤ Active Subscriptions: {active_subs}
▤ Weekly Plans: {weekly_subs}
▤ Monthly Plans: {monthly_subs}

**📱 ACCOUNTS & CAMPAIGNS:**
▤ Telegram Accounts: {total_accounts}
▤ Total Campaigns: {total_campaigns}
▤ Active Campaigns: {active_campaigns}

**🎟️ ACCESS CODES:**
▤ Total Generated: {total_codes}
▤ Used: {used_codes}
▤ Available: {unused_codes}

**📈 SYSTEM:**
▤ Status: ✅ Online
▤ Version: 2.0.0

━━━━━━━━━━━━━━━━━━━
💻 Owner Dashboard
"""
        
        await update.message.reply_text(
            stats_text,
            parse_mode=ParseMode.MARKDOWN
        )
        
    finally:
        db.close()


async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Broadcast message to all users - Owner only"""
    user_id = update.message.from_user.id
    
    if user_id != OWNER_TELEGRAM_ID:
        await update.message.reply_text(
            "🔒 **Access Denied**\n\n"
            "This command is restricted to the owner only."
        )
        return
    
    if len(context.args) < 1:
        await update.message.reply_text(
            "📝 **Usage:**\n"
            "`/broadcast <message>`\n\n"
            "**Example:**\n"
            "`/broadcast Important update: New features added!`\n\n"
            "**Note:** This will send the message to all bot users.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Get the broadcast message
    message = " ".join(context.args)
    
    db = SessionLocal()
    
    try:
        # Get all users
        users = db.query(User).all()
        
        if not users:
            await update.message.reply_text("❌ No users found in database.")
            return
        
        # Send confirmation
        confirm_text = f"""
📢 **BROADCAST CONFIRMATION**
━━━━━━━━━━━━━━━━━━━

**Recipients:** {len(users)} users

**Message:**
{message}

**Ready to send?**
"""
        
        keyboard = [
            [
                InlineKeyboardButton("✅ Send", callback_data=f"broadcast_confirm"),
                InlineKeyboardButton("❌ Cancel", callback_data="broadcast_cancel")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Store broadcast message in context for callback
        context.user_data['broadcast_message'] = message
        context.user_data['broadcast_count'] = len(users)
        
        await update.message.reply_text(
            confirm_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
    finally:
        db.close()


async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user's Telegram profile"""
    user = update.message.from_user
    user_id = user.id
    
    db = SessionLocal()
    
    try:
        # Get user from database
        db_user = db.query(User).filter(User.telegram_user_id == user_id).first()
        
        # Get subscription info
        subscription = None
        if db_user:
            subscription = db.query(Subscription).filter(
                Subscription.user_id == db_user.id,
                Subscription.is_active == True
            ).first()
        
        # Build profile text
        username = f"@{user.username}" if user.username else "No username"
        first_name = user.first_name or "N/A"
        last_name = user.last_name or ""
        full_name = f"{first_name} {last_name}".strip()
        
        language = user.language_code or "Unknown"
        is_bot = "Yes" if user.is_bot else "No"
        is_premium = "✅ Yes" if user.is_premium else "❌ No"
        
        # Subscription status
        if subscription:
            sub_status = "✅ Active"
            sub_plan = subscription.plan_type.upper()
            sub_expiry = format_datetime(subscription.expiry_date)
            days_left = (subscription.expiry_date - datetime.utcnow()).days
            if days_left < 0:
                days_left = 0
        else:
            sub_status = "❌ Inactive"
            sub_plan = "None"
            sub_expiry = "N/A"
            days_left = 0
        
        profile_text = f"""
👤 **YOUR PROFILE**
━━━━━━━━━━━━━━━━━━━

**📱 TELEGRAM INFO:**
▤ Name: {full_name}
▤ Username: {username}
▤ User ID: `{user_id}`
▤ Language: {language}
▤ Premium: {is_premium}
▤ Bot: {is_bot}

**💳 SUBSCRIPTION:**
▤ Status: {sub_status}
▤ Plan: {sub_plan}
▤ Expires: {sub_expiry}
▤ Days Left: {days_left}

**📊 STATS:**
"""
        
        if db_user:
            accounts = db.query(TelegramAccount).filter(
                TelegramAccount.user_id == db_user.id
            ).count()
            
            campaigns = db.query(Campaign).filter(
                Campaign.user_id == db_user.id
            ).count()
            
            profile_text += f"""▤ Telegram Accounts: {accounts}
▤ Campaigns: {campaigns}
"""
        else:
            profile_text += "▤ No data available (use /start first)"
        
        profile_text += "\n━━━━━━━━━━━━━━━━━━━"
        
        keyboard = [
            [InlineKeyboardButton("🚀 Open Dashboard", web_app=WebAppInfo(url=WEBAPP_URL))],
            [InlineKeyboardButton("💳 View Plans", callback_data="view_plans")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            profile_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
    finally:
        db.close()


async def generate_access_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate access code - Owner only"""
    user_id = update.message.from_user.id
    
    if user_id != OWNER_TELEGRAM_ID:
        await update.message.reply_text(
            "🔒 **Access Denied**\n\n"
            "This command is restricted to the owner only."
        )
        return
    
    if len(context.args) < 1:
        await update.message.reply_text(
            "📝 **Usage:**\n"
            "`/generate <plan_type>`\n\n"
            "**Examples:**\n"
            "• `/generate weekly`\n"
            "• `/generate monthly`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    plan_type = context.args[0].lower()
    
    if plan_type not in PLANS:
        await update.message.reply_text(
            f"❌ Invalid plan type!\n\n"
            f"**Available plans:**\n"
            f"• `weekly`\n"
            f"• `monthly`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    db = SessionLocal()
    try:
        # Generate unique code
        while True:
            code = generate_code()
            existing = db.query(AccessCode).filter(AccessCode.code == code).first()
            if not existing:
                break
        
        # Get or create owner user
        owner = db.query(User).filter(User.telegram_user_id == user_id).first()
        if not owner:
            owner = User(
                telegram_user_id=user_id,
                first_name=update.message.from_user.first_name,
                username=update.message.from_user.username,
                is_owner=True
            )
            db.add(owner)
            db.commit()
        
        # Create access code
        access_code = AccessCode(
            code=code,
            plan_type=plan_type,
            created_by=owner.id
        )
        db.add(access_code)
        db.commit()
        
        plan = PLANS[plan_type]
        
        await update.message.reply_text(
            f"✅ **CODE GENERATED**\n"
            f"━━━━━━━━━━━━━━━━━━━\n\n"
            f"**Access Code:** `{code}`\n"
            f"**Plan:** {plan['name']}\n"
            f"**Price:** ₹{plan['price']}\n"
            f"**Duration:** {plan['duration_days']} days\n\n"
            f"**Activation:**\n"
            f"`/redeem {code}`\n\n"
            f"Share this code with users to activate their subscription.",
            parse_mode=ParseMode.MARKDOWN
        )
        
    finally:
        db.close()


async def redeem_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Redeem access code"""
    user_id = update.message.from_user.id
    
    if len(context.args) < 1:
        await update.message.reply_text(
            "📝 **Usage:**\n"
            "`/redeem <code>`\n\n"
            "**Example:**\n"
            "`/redeem ABC123XYZ`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    code = context.args[0].upper()
    db = SessionLocal()
    
    try:
        # Get or create user
        user = db.query(User).filter(User.telegram_user_id == user_id).first()
        if not user:
            user = User(
                telegram_user_id=user_id,
                first_name=update.message.from_user.first_name,
                last_name=update.message.from_user.last_name,
                username=update.message.from_user.username
            )
            db.add(user)
            db.commit()
        
        # Validate code
        access_code = db.query(AccessCode).filter(AccessCode.code == code).first()
        
        if not access_code:
            await update.message.reply_text(
                "❌ **Invalid Code**\n\n"
                "The code you entered is not valid.\n"
                "Please check and try again."
            )
            return
        
        if access_code.is_used:
            await update.message.reply_text(
                "⚠️ **Code Already Used**\n\n"
                "This code has already been redeemed.\n"
                "Contact @spinify for a new code."
            )
            return
        
        # Check for existing subscription
        existing_sub = db.query(Subscription).filter(
            Subscription.user_id == user.id,
            Subscription.is_active == True
        ).first()
        
        if existing_sub and existing_sub.expiry_date > datetime.utcnow():
            await update.message.reply_text(
                f"⚠️ **Active Subscription Exists**\n\n"
                f"**Plan:** {existing_sub.plan_type.upper()}\n"
                f"**Expires:** {format_datetime(existing_sub.expiry_date)}\n\n"
                f"Wait for your current subscription to expire before redeeming a new code."
            )
            return
        
        # Create subscription
        plan = PLANS[access_code.plan_type]
        expiry_date = datetime.utcnow() + timedelta(days=plan["duration_days"])
        
        subscription = Subscription(
            user_id=user.id,
            plan_type=access_code.plan_type,
            price=plan["price"],
            expiry_date=expiry_date,
            is_active=True
        )
        db.add(subscription)
        
        # Mark code as used
        access_code.is_used = True
        access_code.used_by = user.id
        access_code.used_at = datetime.utcnow()
        
        db.commit()
        
        keyboard = [[
            InlineKeyboardButton("🚀 Open Dashboard", web_app=WebAppInfo(url=WEBAPP_URL))
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"🎉 **SUBSCRIPTION ACTIVATED!**\n"
            f"━━━━━━━━━━━━━━━━━━━\n\n"
            f"**Plan:** {plan['name']}\n"
            f"**Price:** ₹{plan['price']}\n"
            f"**Valid Until:** {format_datetime(expiry_date)}\n"
            f"**Duration:** {plan['duration_days']} days\n\n"
            f"✨ All premium features unlocked!\n"
            f"Click 'Open Dashboard' to start your campaign.\n\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"💻 Developer: @spinify",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
    finally:
        db.close()


# =====================
# CALLBACK HANDLERS
# =====================

async def broadcast_confirm_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send broadcast message to all users"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    if user_id != OWNER_TELEGRAM_ID:
        await query.edit_message_text("🔒 Access Denied")
        return
    
    message = context.user_data.get('broadcast_message')
    
    if not message:
        await query.edit_message_text("❌ Broadcast message not found!")
        return
    
    db = SessionLocal()
    
    try:
        users = db.query(User).all()
        
        sent = 0
        failed = 0
        
        await query.edit_message_text(
            f"📤 **Broadcasting...**\n\n"
            f"Sending to {len(users)} users...",
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Send to each user
        for user in users:
            try:
                broadcast_text = f"""
📢 **BROADCAST MESSAGE**
━━━━━━━━━━━━━━━━━━━

{message}

━━━━━━━━━━━━━━━━━━━
From: @spinify (Owner)
"""
                await context.bot.send_message(
                    chat_id=user.telegram_user_id,
                    text=broadcast_text,
                    parse_mode=ParseMode.MARKDOWN
                )
                sent += 1
            except Exception as e:
                logger.error(f"Failed to send to {user.telegram_user_id}: {e}")
                failed += 1
        
        # Send completion report
        await query.edit_message_text(
            f"✅ **BROADCAST COMPLETE**\n\n"
            f"▤ Total: {len(users)}\n"
            f"▤ Sent: {sent}\n"
            f"▤ Failed: {failed}",
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Clear context data
        context.user_data.pop('broadcast_message', None)
        context.user_data.pop('broadcast_count', None)
        
    finally:
        db.close()


async def broadcast_cancel_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel broadcast"""
    query = update.callback_query
    await query.answer()
    
    # Clear context data
    context.user_data.pop('broadcast_message', None)
    context.user_data.pop('broadcast_count', None)
    
    await query.edit_message_text(
        "❌ **Broadcast Cancelled**\n\n"
        "No messages were sent.",
        parse_mode=ParseMode.MARKDOWN
    )

async def campaign_settings_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show campaign settings (callback version)"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    db = SessionLocal()
    
    try:
        user = db.query(User).filter(User.telegram_user_id == user_id).first()
        
        if not user:
            await query.edit_message_text("❌ No account found!\n\nUse /start first.")
            return
        
        campaign = db.query(Campaign).filter(Campaign.user_id == user.id).first()
        
        if campaign:
            interval = campaign.interval_minutes
            night_mode = "✅ ON" if campaign.night_mode_enabled else "❌ OFF"
            groups_count = len(campaign.groups) if campaign.groups else 0
        else:
            interval = 60
            night_mode = "❌ OFF"
            groups_count = 0
        
        settings_text = f"""
⚙️ **CAMPAIGN SETTINGS**
━━━━━━━━━━━━━━━━━━━

**📊 Current Config:**
▤ Interval: {interval} minutes
▤ Message Delay: 60 sec
▤ Group Gap: 60 sec
▤ Night Mode: {night_mode}
▤ Groups: {groups_count}

**🔧 Configure:**
"""
        
        keyboard = [
            [InlineKeyboardButton("⏰ Change Interval", callback_data="set_interval")],
            [InlineKeyboardButton("⏱️ Change Delays", callback_data="set_delays")],
            [InlineKeyboardButton("🌙 Toggle Night Mode", callback_data="toggle_night_mode")],
            [InlineKeyboardButton("👥 Manage Groups", callback_data="manage_groups")],
            [InlineKeyboardButton("« Back", callback_data="back_to_start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            settings_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
    finally:
        db.close()


async def set_interval_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set campaign interval"""
    query = update.callback_query
    await query.answer()
    
    interval_text = """
⏰ **SET INTERVAL**
━━━━━━━━━━━━━━━━━━━

Select campaign interval:
(Minimum: 20 minutes)
"""
    
    keyboard = [
        [
            InlineKeyboardButton("20 min", callback_data="interval_20"),
            InlineKeyboardButton("30 min", callback_data="interval_30")
        ],
        [
            InlineKeyboardButton("45 min", callback_data="interval_45"),
            InlineKeyboardButton("60 min", callback_data="interval_60")
        ],
        [
            InlineKeyboardButton("90 min", callback_data="interval_90"),
            InlineKeyboardButton("120 min", callback_data="interval_120")
        ],
        [
            InlineKeyboardButton("180 min", callback_data="interval_180"),
            InlineKeyboardButton("240 min", callback_data="interval_240")
        ],
        [InlineKeyboardButton("« Back", callback_data="campaign_settings")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        interval_text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )


async def interval_selected_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle interval selection"""
    query = update.callback_query
    await query.answer()
    
    # Extract interval from callback data
    interval = int(query.data.split("_")[1])
    user_id = query.from_user.id
    db = SessionLocal()
    
    try:
        user = db.query(User).filter(User.telegram_user_id == user_id).first()
        if not user:
            await query.edit_message_text("❌ No account found!")
            return
        
        campaign = db.query(Campaign).filter(Campaign.user_id == user.id).first()
        
        if campaign:
            campaign.interval_minutes = interval
            db.commit()
            
            await query.edit_message_text(
                f"✅ **Interval Updated!**\n\n"
                f"New interval: **{interval} minutes**\n\n"
                f"Your campaign will run every {interval} minutes.",
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await query.edit_message_text(
                "⚠️ **No Campaign Found**\n\n"
                "Create a campaign in the dashboard first!",
                parse_mode=ParseMode.MARKDOWN
            )
        
    finally:
        db.close()


async def set_delays_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show delay settings"""
    query = update.callback_query
    await query.answer()
    
    delay_text = """
⏱️ **DELAY SETTINGS**
━━━━━━━━━━━━━━━━━━━

**Current Delays:**
▤ Message Delay: 60 sec (fixed)
▤ Group Gap: 60 sec (fixed)

**Why 60 seconds?**
━━━━━━━━━━━━━━━━━━━
▤ Prevents spam detection
▤ Avoids Telegram limits
▤ Ensures reliable delivery
▤ Maintains account safety

**Note:** Delays are optimized for safety and cannot be changed to maintain compliance with Telegram's terms.
"""
    
    keyboard = [[InlineKeyboardButton("« Back", callback_data="campaign_settings")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        delay_text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )


async def toggle_night_mode_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Toggle night mode on/off"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    db = SessionLocal()
    
    try:
        user = db.query(User).filter(User.telegram_user_id == user_id).first()
        if not user:
            await query.edit_message_text("❌ No account found!")
            return
        
        campaign = db.query(Campaign).filter(Campaign.user_id == user.id).first()
        
        if campaign:
            # Toggle night mode
            campaign.night_mode_enabled = not campaign.night_mode_enabled
            db.commit()
            
            status = "✅ ENABLED" if campaign.night_mode_enabled else "❌ DISABLED"
            
            night_text = f"""
🌙 **NIGHT MODE {status}**
━━━━━━━━━━━━━━━━━━━

**Status:** {status}

**Schedule:**
▤ Pause Time: 10:00 PM
▤ Resume Time: 6:00 AM

**Benefits:**
▤ Avoid late-night spam
▤ Better engagement rates
▤ Respectful timing
▤ Account safety
"""
            
            keyboard = [
                [InlineKeyboardButton("🔄 Toggle Again", callback_data="toggle_night_mode")],
                [InlineKeyboardButton("« Back", callback_data="campaign_settings")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                night_text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await query.edit_message_text(
                "⚠️ **No Campaign Found**\n\n"
                "Create a campaign in the dashboard first!",
                parse_mode=ParseMode.MARKDOWN
            )
        
    finally:
        db.close()


async def manage_groups_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show group management"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    db = SessionLocal()
    
    try:
        user = db.query(User).filter(User.telegram_user_id == user_id).first()
        if not user:
            await query.edit_message_text("❌ No account found!")
            return
        
        campaign = db.query(Campaign).filter(Campaign.user_id == user.id).first()
        
        if campaign and campaign.groups:
            groups = campaign.groups
            groups_list = "\n".join([f"▤ {i+1}. {group}" for i, group in enumerate(groups[:10])])
            
            groups_text = f"""
👥 **GROUP MANAGEMENT**
━━━━━━━━━━━━━━━━━━━

**Current Groups ({len(groups)}/10):**
{groups_list}

**Note:** Use the web dashboard to add/remove groups.

**Dashboard:** {WEBAPP_URL}
"""
        else:
            groups_text = """
👥 **GROUP MANAGEMENT**
━━━━━━━━━━━━━━━━━━━

**No Groups Added**

**To Add Groups:**
▤ Open the web dashboard
▤ Go to Step 3
▤ Add group links (max 10)
▤ Save configuration

**Dashboard:** """ + WEBAPP_URL
        
        keyboard = [
            [InlineKeyboardButton("🚀 Open Dashboard", web_app=WebAppInfo(url=WEBAPP_URL))],
            [InlineKeyboardButton("« Back", callback_data="campaign_settings")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            groups_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
    finally:
        db.close()

async def cmd_profile_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user profile (callback version)"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    user_id = user.id
    
    db = SessionLocal()
    
    try:
        # Get user from database
        db_user = db.query(User).filter(User.telegram_user_id == user_id).first()
        
        # Get subscription info
        subscription = None
        if db_user:
            subscription = db.query(Subscription).filter(
                Subscription.user_id == db_user.id,
                Subscription.is_active == True
            ).first()
        
        # Build profile info
        username = f"@{user.username}" if user.username else "No username"
        first_name = user.first_name or "N/A"
        last_name = user.last_name or ""
        full_name = f"{first_name} {last_name}".strip()
        
        language = user.language_code or "Unknown"
        is_bot = "Yes" if user.is_bot else "No"
        is_premium = "✅ Yes" if user.is_premium else "❌ No"
        
        # Subscription status
        if subscription:
            sub_status = "✅ Active"
            sub_plan = subscription.plan_type.upper()
            sub_expiry = format_datetime(subscription.expiry_date)
            days_left = (subscription.expiry_date - datetime.utcnow()).days
            if days_left < 0:
                days_left = 0
        else:
            sub_status = "❌ Inactive"
            sub_plan = "None"
            sub_expiry = "N/A"
            days_left = 0
        
        profile_text = f"""
👤 **YOUR PROFILE**
━━━━━━━━━━━━━━━━━━━

**📱 TELEGRAM INFO:**
▤ Name: {full_name}
▤ Username: {username}
▤ User ID: `{user_id}`
▤ Language: {language}
▤ Premium: {is_premium}
▤ Bot: {is_bot}

**💳 SUBSCRIPTION:**
▤ Status: {sub_status}
▤ Plan: {sub_plan}
▤ Expires: {sub_expiry}
▤ Days Left: {days_left}

**📊 STATS:**
"""
        
        if db_user:
            accounts = db.query(TelegramAccount).filter(
                TelegramAccount.user_id == db_user.id
            ).count()
            
            campaigns = db.query(Campaign).filter(
                Campaign.user_id == db_user.id
            ).count()
            
            profile_text += f"""▤ Telegram Accounts: {accounts}
▤ Campaigns: {campaigns}
"""
        else:
            profile_text += "▤ No data available (use /start first)"
        
        profile_text += "\n━━━━━━━━━━━━━━━━━━━"
        
        keyboard = [
            [InlineKeyboardButton("🚀 Open Dashboard", web_app=WebAppInfo(url=WEBAPP_URL))],
            [InlineKeyboardButton("💳 View Plans", callback_data="view_plans")],
            [InlineKeyboardButton("« Back", callback_data="back_to_start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            profile_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
    finally:
        db.close()


async def my_status_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user status (callback version)"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    db = SessionLocal()
    
    try:
        stats = get_user_stats(db, user_id)
        
        if not stats:
            await query.edit_message_text(
                "❌ **No Account Found**\n\n"
                "Use /start to initialize your account."
            )
            return
        
        sub = stats["subscription"]
        sub_status = "✅ Active" if sub else "❌ Inactive"
        sub_plan = sub.plan_type.upper() if sub else "None"
        sub_expiry = format_datetime(sub.expiry_date) if sub else "N/A"
        
        if sub and sub.expiry_date:
            days_left = (sub.expiry_date - datetime.utcnow()).days
            if days_left < 0:
                days_left = 0
        else:
            days_left = 0
        
        status_message = f"""
📊 **YOUR STATUS**
━━━━━━━━━━━━━━━━━━━

**👤 Account:**
▤ Status: {sub_status}
▤ Plan: {sub_plan}
▤ Days Left: {days_left}
▤ Expires: {sub_expiry}

**📱 Resources:**
▤ Accounts: {stats["accounts"]}
▤ Campaigns: {stats["campaigns"]}
"""
        
        if not sub or days_left <= 0:
            status_message += "\n⚠️ **Subscription inactive!**\nUse `/redeem <code>` to activate."
        
        keyboard = [
            [InlineKeyboardButton("🚀 Open Dashboard", web_app=WebAppInfo(url=WEBAPP_URL))],
            [InlineKeyboardButton("💳 View Plans", callback_data="view_plans")],
            [InlineKeyboardButton("« Back", callback_data="back_to_start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            status_message,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
    finally:
        db.close()


async def view_plans(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show subscription plans"""
    query = update.callback_query
    await query.answer()
    
    plans_message = """
💳 **SUBSCRIPTION PLANS**
━━━━━━━━━━━━━━━━━━━

📦 **WEEKLY PLAN**
▤ Price: ₹99
▤ Duration: 7 days
▤ All features included
▤ Perfect for testing

📦 **MONTHLY PLAN** ⭐
▤ Price: ₹299
▤ Duration: 30 days
▤ All features included
▤ **Best Value!**

**✨ INCLUDED FEATURES:**
▤ Multi-account management
▤ Smart scheduling
▤ Night mode automation
▤ Auto-reply system
▤ Up to 10 groups per campaign
▤ Real-time control

**💰 HOW TO SUBSCRIBE:**
1️⃣ Get access code from @spinify
2️⃣ Use `/redeem <code>` to activate
3️⃣ Start using all premium features

━━━━━━━━━━━━━━━━━━━
💻 Contact: @spinify
"""
    
    keyboard = [[InlineKeyboardButton("« Back", callback_data="back_to_start")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        plans_message,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )


async def help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help (callback version)"""
    query = update.callback_query
    await query.answer()
    
    help_text = """
📖 **HELP & COMMANDS**
━━━━━━━━━━━━━━━━━━━

**👤 USER COMMANDS:**
▤ `/start` - Welcome menu
▤ `/help` - Show this help
▤ `/status` - Your statistics
▤ `/settings` - Campaign config
▤ `/redeem <code>` - Activate plan

**👑 OWNER ONLY:**
▤ `/generate weekly`
▤ `/generate monthly`

**💡 GETTING STARTED:**
1️⃣ Click "Open Dashboard"
2️⃣ Add Telegram account with API credentials
3️⃣ Enter phone & verify OTP
4️⃣ Add groups and messages
5️⃣ Configure & start campaign

**🔑 API CREDENTIALS:**
Get from: my.telegram.org/apps

**🆘 SUPPORT:**
Contact @spinify for help

━━━━━━━━━━━━━━━━━━━
"""
    
    keyboard = [[InlineKeyboardButton("« Back", callback_data="back_to_start")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        help_text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )


async def about_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show about information"""
    query = update.callback_query
    await query.answer()
    
    about_text = """
ℹ️ **ABOUT SPINIFY ADS**
━━━━━━━━━━━━━━━━━━━

**🚀 Version:** 2.0.0
**📅 Updated:** January 2026

**📝 DESCRIPTION:**
Spinify Ads is a powerful Telegram automation platform for scheduling and sending advertisements to multiple groups with smart features.

**🌟 KEY FEATURES:**
▤ Multi-account support
▤ OTP & 2FA authentication
▤ Smart scheduling (20min-4hrs)
▤ Night mode (10PM-6AM pause)
▤ Auto-reply system
▤ Bulk posting (10 groups)
▤ Real-time campaign control
▤ Secure session management

**🛠️ TECHNOLOGY:**
▤ Python + Telethon
▤ FastAPI Backend
▤ SQLite/PostgreSQL Database
▤ Modern Web Dashboard

**💻 DEVELOPER:**
@spinify

**🔗 SUPPORT:**
For help, questions, or custom features, contact @spinify

━━━━━━━━━━━━━━━━━━━
Made with ❤️ by @spinify
"""
    
    keyboard = [[InlineKeyboardButton("« Back", callback_data="back_to_start")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        about_text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )


async def back_to_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Return to start menu with premium card"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    user_id = user.id
    
    db = SessionLocal()
    
    try:
        # Get user from database
        db_user = db.query(User).filter(User.telegram_user_id == user_id).first()
        
        # Get subscription info
        subscription = None
        if db_user:
            subscription = db.query(Subscription).filter(
                Subscription.user_id == db_user.id,
                Subscription.is_active == True
            ).first()
        
        # Build profile info
        username = f"@{user.username}" if user.username else "Guest"
        first_name = user.first_name or "User"
        is_premium = user.is_premium if hasattr(user, 'is_premium') else False
        premium_badge = "👑 PREMIUM" if is_premium else "STANDARD"
        
        # Subscription status
        if subscription:
            sub_badge = "✅ ACTIVE"
            sub_plan = subscription.plan_type.upper()
            days_left = (subscription.expiry_date - datetime.utcnow()).days
            if days_left < 0:
                days_left = 0
        else:
            sub_badge = "⚠️ INACTIVE"
            sub_plan = "FREE"
            days_left = 0
        
        keyboard = [
            [
                InlineKeyboardButton(
                    "🚀 Open Dashboard",
                    web_app=WebAppInfo(url=WEBAPP_URL)
                )
            ],
            [
                InlineKeyboardButton("👤 Profile", callback_data="cmd_profile"),
                InlineKeyboardButton("📊 Status", callback_data="my_status")
            ],
            [
                InlineKeyboardButton("⚙️ Settings", callback_data="campaign_settings"),
                InlineKeyboardButton("💳 Plans", callback_data="view_plans")
            ],
            [
                InlineKeyboardButton("📖 Help", callback_data="help"),
                InlineKeyboardButton("ℹ️ About", callback_data="about")
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Telegram profile-style welcome
        welcome_message = f"""
          🎭
     ━━━━━━━━━━━━━━

**{first_name}**
{username}

┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ **Profile**                      
┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛

ID: `{user_id}`
Tier: {premium_badge}

💳 **Subscription**
Plan: {sub_plan} {sub_badge}
Days Left: **{days_left}** days

━━━━━━━━━━━━━━━━━━━━━━━━━━

**🌟 SPINIFY ADS**
Premium Ad Automation

▤ Multi-Account Management
▤ Smart Scheduling (20-240min)
▤ Night Mode (10PM-6AM)
▤ Auto-Reply System
▤ Bulk Posting (10 groups)
▤ Secure OTP & 2FA

**💰 Plans**
▤ Weekly: ₹99 (7 days)
▤ Monthly: ₹299 (30 days) ⭐

━━━━━━━━━━━━━━━━━━━━━━━━━━
💻 @spinify
"""
        
        await query.edit_message_text(
            welcome_message,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
    finally:
        db.close()


# =====================
# MAIN
# =====================

def main():
    """Start the bot"""
    logger.info("🚀 Starting Spinify Ads Bot...")
    
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CommandHandler("settings", settings_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("broadcast", broadcast_command))
    app.add_handler(CommandHandler("profile", profile_command))
    app.add_handler(CommandHandler("generate", generate_access_code))
    app.add_handler(CommandHandler("redeem", redeem_code))
    
    # Callback handlers - Broadcast
    app.add_handler(CallbackQueryHandler(broadcast_confirm_callback, pattern="broadcast_confirm"))
    app.add_handler(CallbackQueryHandler(broadcast_cancel_callback, pattern="broadcast_cancel"))
    
    # Callback handlers - Campaign Settings
    app.add_handler(CallbackQueryHandler(campaign_settings_callback, pattern="campaign_settings"))
    app.add_handler(CallbackQueryHandler(set_interval_callback, pattern="set_interval"))
    app.add_handler(CallbackQueryHandler(interval_selected_callback, pattern="^interval_\\d+$"))
    app.add_handler(CallbackQueryHandler(set_delays_callback, pattern="set_delays"))
    app.add_handler(CallbackQueryHandler(toggle_night_mode_callback, pattern="toggle_night_mode"))
    app.add_handler(CallbackQueryHandler(manage_groups_callback, pattern="manage_groups"))
    
    # Callback handlers - General
    app.add_handler(CallbackQueryHandler(cmd_profile_callback, pattern="cmd_profile"))
    app.add_handler(CallbackQueryHandler(my_status_callback, pattern="my_status"))
    app.add_handler(CallbackQueryHandler(view_plans, pattern="view_plans"))
    app.add_handler(CallbackQueryHandler(help_callback, pattern="help"))
    app.add_handler(CallbackQueryHandler(about_callback, pattern="about"))
    app.add_handler(CallbackQueryHandler(back_to_start, pattern="back_to_start"))
    
    logger.info(f"📱 Owner ID: {OWNER_TELEGRAM_ID}")
    logger.info(f"🌐 WebApp URL: {WEBAPP_URL}")
    logger.info("✅ Bot is running and ready!")
    
    # Run the bot
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
