from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import random
import os

# Bot Token & Channels (یہ Railway کی Env Variables سے اٹھائے گا)
TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_CHANNEL = os.getenv("TELEGRAM_CHANNEL")
WHATSAPP_LINK = os.getenv("WHATSAPP_LINK")

# Prediction Logic
def get_prediction():
    result = random.choice(["Big", "Small"])
    amount = random.randint(10, 100)
    chance = random.randint(50, 95)
    return f"🎲 **Prediction:** {result}\n💰 **Bet Amount:** {amount}\n🎯 **Winning Chance:** {chance}%"

# Start Command
def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    keyboard = [
        [InlineKeyboardButton("✅ Join WhatsApp Channel", url=WHATSAPP_LINK)],
        [InlineKeyboardButton("✅ Join Telegram Channel", url=f"https://t.me/TW_Broken{TELEGRAM_CHANNEL}")],
        [InlineKeyboardButton("🔄 Check & Continue", callback_data="check_join")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(f"👋 Welcome {user.first_name}!\n\n📌 To continue, please join both channels first:", reply_markup=reply_markup)

# Check Subscription
def check_join(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    member = context.bot.get_chat_member(chat_id=TELEGRAM_CHANNEL, user_id=user_id)
    
    if member.status in ["member", "administrator", "creator"]:
        keyboard = [
            [InlineKeyboardButton("⚡ Wingo 30 Seconds", callback_data="wingo_30s")],
            [InlineKeyboardButton("⏳ Wingo 1 Minute", callback_data="wingo_1m")],
            [InlineKeyboardButton("⏲️ Wingo 3 Minutes", callback_data="wingo_3m")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("✅ You have joined both channels!\n\n🎮 Choose a game:", reply_markup=reply_markup)
    else:
        query.message.reply_text("❌ Please join both channels first!")

# Handle Wingo Buttons
def wingo(update: Update, context: CallbackContext):
    query = update.callback_query
    prediction = get_prediction()
    query.message.reply_text(prediction)

# Main Function
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(check_join, pattern="check_join"))
    dp.add_handler(CallbackQueryHandler(wingo, pattern="wingo_30s"))
    dp.add_handler(CallbackQueryHandler(wingo, pattern="wingo_1m"))
    dp.add_handler(CallbackQueryHandler(wingo, pattern="wingo_3m"))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
