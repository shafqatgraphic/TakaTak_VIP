import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext

# ✅ Env Variables (Railway ke liye)
TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_CHANNEL = os.getenv("TELEGRAM_CHANNEL")
WHATSAPP_LINK = os.getenv("WHATSAPP_LINK")

# 🎲 Prediction Logic
def get_prediction():
    result = random.choice(["Big", "Small"])
    amount = random.randint(10, 100)
    chance = random.randint(50, 95)
    return f"🎲 **Prediction:** {result}\n💰 **Bet Amount:** {amount}\n🎯 **Winning Chance:** {chance}%"

# 🚀 Start Command
async def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    keyboard = [
        [InlineKeyboardButton("✅ Join WhatsApp Channel", url=WHATSAPP_LINK)],
        [InlineKeyboardButton("✅ Join Telegram Channel", url=f"https://t.me/{TELEGRAM_CHANNEL}")],
        [InlineKeyboardButton("🔄 Check & Continue", callback_data="check_join")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f"👋 Welcome {user.first_name}!\n\n📌 To continue, please join both channels first:", reply_markup=reply_markup)

# 🔄 Check Subscription
async def check_join(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    
    try:
        member = await context.bot.get_chat_member(chat_id=TELEGRAM_CHANNEL, user_id=user_id)
        if member.status in ["member", "administrator", "creator"]:
            keyboard = [
                [InlineKeyboardButton("⚡ Wingo 30 Seconds", callback_data="wingo_30s")],
                [InlineKeyboardButton("⏳ Wingo 1 Minute", callback_data="wingo_1m")],
                [InlineKeyboardButton("⏲️ Wingo 3 Minutes", callback_data="wingo_3m")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text("✅ You have joined both channels!\n\n🎮 Choose a game:", reply_markup=reply_markup)
        else:
            await query.message.reply_text("❌ Please join both channels first!")
    except Exception as e:
        await query.message.reply_text("⚠️ Error checking subscription. Try again!")

# 🎮 Handle Wingo Predictions
async def wingo(update: Update, context: CallbackContext):
    query = update.callback_query
    prediction = get_prediction()
    await query.message.reply_text(prediction)

# 🔥 Main Function
def main():
    app = Application.builder().token(TOKEN).build()

    # ✅ Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_join, pattern="check_join"))
    app.add_handler(CallbackQueryHandler(wingo, pattern="wingo_30s"))
    app.add_handler(CallbackQueryHandler(wingo, pattern="wingo_1m"))
    app.add_handler(CallbackQueryHandler(wingo, pattern="wingo_3m"))

    # 🚀 Start Bot
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
