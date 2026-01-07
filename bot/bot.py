from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

BOT_TOKEN = "8554290865:AAH1qQ0jOSkdj7A6LGCP1rm_KWvCgp_jaqs"
WEBAPP_URL = "https://cinetimetv.store/webapp"  # change later


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(
                "🚀 Open Dashboard",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        ],
        [
            InlineKeyboardButton("▶ Start Ads", callback_data="start_ads"),
            InlineKeyboardButton("⏹ Stop Ads", callback_data="stop_ads")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Welcome 👋\n\n"
        "Use the dashboard to:\n"
        "• Login Telegram account\n"
        "• Add groups\n"
        "• Schedule ads\n\n"
        "Control sending using buttons below.",
        reply_markup=reply_markup
    )


async def start_ads(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # later → call backend API
    await query.edit_message_text(
        "✅ Scheduler started.\n\n"
        "Ads will be sent using your saved settings."
    )


async def stop_ads(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # later → call backend API
    await query.edit_message_text(
        "⏹ Scheduler stopped.\n\n"
        "No ads will be sent until restarted."
    )


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("startads", start_ads))
    app.add_handler(CommandHandler("stopads", stop_ads))

    print("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
