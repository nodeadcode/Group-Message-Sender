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
import random
import string
from datetime import datetime, timedelta
import sys
import os

# Add backend to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from database import SessionLocal
from models import User, AccessCode, Subscription, TelegramAccount
from config import OWNER_TELEGRAM_ID, PLANS, BOT_TOKEN, WEBAPP_URL


def generate_code(length=10):
    """Generate a random access code"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    
    keyboard = [
        [
            InlineKeyboardButton(
                "🚀 Open Dashboard",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        ],
        [
            InlineKeyboardButton("💳 View Plans", callback_data="view_plans"),
        ],
        [
            InlineKeyboardButton("▶ Start Ads", callback_data="start_ads"),
            InlineKeyboardButton("⏹ Stop Ads", callback_data="stop_ads")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_message = f"""
🎉 **Welcome to Spinify Ads, {user.first_name}!** 🎉

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 **Your Smart Telegram Ad Automation Platform**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ **Premium Features:**

📱 **Multi-Account Management**
   • Connect multiple Telegram accounts
   • Switch between accounts seamlessly
   
🔄 **Smart Auto-Forwarding**
   • Forward ads via Saved Messages
   • Automated posting to groups
   
⏰ **Intelligent Scheduling**
   • Custom intervals (20min - 4hrs)
   • Set it and forget it
   
🌙 **Night Mode Protection**
   • Auto-pause: 12 AM - 6 AM
   • Respect user sleep time
   
🤖 **Auto-Reply System**
   • Respond to personal messages
   • Customizable reply messages
   
💬 **Bulk Group Posting**
   • Send to up to 10 groups
   • Smart delay management
   
🎯 **Real-Time Control**
   • Start/Stop campaigns instantly
   • Monitor from anywhere

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 **Subscription Plans:**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 **Weekly**  → ₹99  (7 days)
📦 **Monthly** → ₹299 (30 days)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 **Quick Commands:**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• `/start` - Show this menu
• `/redeem <code>` - Activate subscription

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👉 Click **"🚀 Open Dashboard"** below to start!
"""

    await update.message.reply_text(
        welcome_message,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


async def generate_access_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate access code - Owner only command"""
    user_id = update.message.from_user.id
    
    # Check if user is owner
    if user_id != OWNER_TELEGRAM_ID:
        await update.message.reply_text("❌ This command is only for the owner.")
        return
    
# Parse command arguments
    if len(context.args) < 1:
        await update.message.reply_text(
            "Usage: /generate <plan_type>\n\n"
            "Examples:\n"
            "  /generate weekly\n"
            "  /generate monthly"
        )
        return
    
    plan_type = context.args[0].lower()
    
    if plan_type not in PLANS:
        await update.message.reply_text(f"❌ Invalid plan type. Use 'weekly' or 'monthly'")
        return
    
    # Generate unique code
    db = SessionLocal()
    try:
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
            f"✅ **Code Generated Successfully!**\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🎟️ **Access Code:** `{code}`\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📦 **Plan Details:**\n"
            f"• Name: {plan['name']}\n"
            f"• Price: ₹{plan['price']}\n"
            f"• Duration: {plan['duration_days']} days\n\n"
            f"💡 **Instructions:**\n"
            f"Share this code with users to activate their subscription.\n\n"
            f"User activation command:\n"
            f"`/redeem {code}`",
            parse_mode="Markdown"
        )
        
    finally:
        db.close()


async def redeem_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Redeem access code - All users"""
    user_id = update.message.from_user.id
    
    # Parse command arguments
    if len(context.args) < 1:
        await update.message.reply_text(
            "Usage: /redeem <code>\n\n"
            "Example:\n"
            "  /redeem ABC123XYZ"
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
            await update.message.reply_text("❌ Invalid code. Please check and try again.")
            return
        
        if access_code.is_used:
            await update.message.reply_text(
                "❌ This code has already been used.\n\n"
                "Please contact the owner for a new code."
            )
            return
        
        # Check if user already has an active subscription
        existing_sub = db.query(Subscription).filter(
            Subscription.user_id == user.id,
            Subscription.is_active == True
        ).first()
        
        if existing_sub:
            # Auto-expire if past expiry date
            if existing_sub.expiry_date < datetime.utcnow():
                existing_sub.is_active = False
                db.commit()
            else:
                await update.message.reply_text(
                    f"⚠️ You already have an active subscription!\n\n"
                    f"Plan: {existing_sub.plan_type}\n"
                    f"Expires: {existing_sub.expiry_date.strftime('%Y-%m-%d %H:%M')}\n\n"
                    f"Wait for it to expire before redeeming a new code."
                )
                return
        
        # Get plan details
        plan = PLANS[access_code.plan_type]
        expiry_date = datetime.utcnow() + timedelta(days=plan["duration_days"])
        
        # Create subscription
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
        
        await update.message.reply_text(
            f"🎉 **Subscription Activated!** 🎉\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📦 **Plan:** {plan['name']}\n"
            f"💰 **Price:** ₹{plan['price']}\n"
            f"📅 **Valid Until:** {expiry_date.strftime('%d %b %Y, %I:%M %p')}\n"
            f"⏱️ **Duration:** {plan['duration_days']} days\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"✨ **You're all set!**\n"
            f"All premium features are now unlocked.\n\n"
            f"🚀 Open the dashboard to start your first campaign!",
            parse_mode="Markdown"
        )
        
    finally:
        db.close()


async def start_ads(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    db = SessionLocal()
    
    try:
        # Check if user exists
        user = db.query(User).filter(User.telegram_user_id == user_id).first()
        if not user:
            await query.edit_message_text(
                "❌ Please open the dashboard first!\n\n"
                f"Visit: {WEBAPP_URL}"
            )
            return
        
        # Check if user has added telegram accounts
        accounts_count = db.query(TelegramAccount).filter(
            TelegramAccount.user_id == user.id,
            TelegramAccount.is_active == True
        ).count()
        
        if accounts_count == 0:
            await query.edit_message_text(
                "⚠️ No Telegram accounts added!\n\n"
                "To start ads:\n"
                "1. Open dashboard\n"
                "2. Add your Telegram account  \n"
                "3. Create campaign\n\n"
                f"Dashboard: {WEBAPP_URL}"
            )
            return
        
        # Check subscription
        subscription = db.query(Subscription).filter(
            Subscription.user_id == user.id,
            Subscription.is_active == True
        ).first()
        
        if not subscription:
            await query.edit_message_text(
                "⚠️ No active subscription!\n\n"
                "Use /redeem CODE first."
            )
            return
        
        await query.edit_message_text(
            f"✅ Campaign starting...\n\n"
            f"📱 Accounts: {accounts_count}\n"
            f"💳 Plan: {subscription.plan_type}\n\n"
            f"Manage: {WEBAPP_URL}"
        )
    finally:
        db.close()


async def stop_ads(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # later → call backend API
    await query.edit_message_text(
        "⏹ Scheduler stopped.\n\n"
        "No ads will be sent until restarted."
    )


async def view_plans(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show subscription plans"""
    query = update.callback_query
    await query.answer()
    
    plans_message = """
💳 **Subscription Plans** 💳

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 **Weekly Plan**
💰 Price: **₹99**
📅 Duration: **7 days**
✨ All Features Included
🎯 Perfect for testing!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 **Monthly Plan** ⭐ *BEST VALUE*
💰 Price: **₹299**
📅 Duration: **30 days**
✨ All Features Included
🚀 Recommended for serious users!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎟️ **How to Subscribe:**

1️⃣ Get an access code from [@spinify](https://t.me/spinify)
2️⃣ Use `/redeem <code>` to activate
3️⃣ Start using premium features!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 **Payment Methods:**

• 💳 Razorpay (UPI, Cards, Net Banking)
• 🪙 Crypto (BTC, ETH, USDT, etc.)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📱 Contact [@spinify](https://t.me/spinify) for codes!
"""
    
    keyboard = [[InlineKeyboardButton("« Back", callback_data="back_to_start")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        plans_message,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


async def back_to_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Return to start message"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    
    keyboard = [
        [
            InlineKeyboardButton(
                "🚀 Open Dashboard",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        ],
        [
            InlineKeyboardButton("💳 View Plans", callback_data="view_plans"),
        ],
        [
            InlineKeyboardButton("▶ Start Ads", callback_data="start_ads"),
            InlineKeyboardButton("⏹ Stop Ads", callback_data="stop_ads")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_message = f"""
🎉 **Welcome to Spinify Ads, {user.first_name}!**

Your all-in-one solution for automated Telegram group advertising.

✨ **Features:**
• 📱 Multi-account management
• 🔄 Auto-forward via Saved Messages
• ⏰ Smart scheduling with intervals
• 🌙 Night mode (12 AM - 6 AM)
• 🤖 Auto-reply to personal messages
• 💬 Send to up to 10 groups
• 🎯 Real-time campaign control

💰 **Subscription Plans:**
• Weekly: ₹99 (7 days)
• Monthly: ₹299 (30 days)

📝 **Quick Commands:**
• `/redeem <code>` - Activate subscription
• `/start` - Show this message

👉 Click **"Open Dashboard"** to get started!
"""

    await query.edit_message_text(
        welcome_message,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


def main():
    """Start the bot"""
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("generate", generate_access_code))
    app.add_handler(CommandHandler("redeem", redeem_code))
    app.add_handler(CallbackQueryHandler(start_ads, pattern="start_ads"))
    app.add_handler(CallbackQueryHandler(stop_ads, pattern="stop_ads"))
    app.add_handler(CallbackQueryHandler(view_plans, pattern="view_plans"))
    app.add_handler(CallbackQueryHandler(back_to_start, pattern="back_to_start"))

    print("🤖 Bot is running...")
    print(f"📱 Owner ID: {OWNER_TELEGRAM_ID}")
    print(f"🌐 WebApp URL: {WEBAPP_URL}")
    
    # Run the bot
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
