import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, filters

# ✅ Env Variables (Railway ke liye)
TOKEN = os.getenv("BOT_TOKEN")
WHATSAPP_LINK = os.getenv("WHATSAPP_LINK")

# 🎲 Prediction Logic
def get_signal(time_frame, period):
    signal_color = random.choice(["GREEN", "RED"])
    signal_size = random.choice(["BIG", "SMALL"])
    win_rate = random.randint(75, 95)
    
    return f"""🎯 **PREMIUM SIGNAL**  
━━━━━━━━━━━━━━  
📊 **SIGNAL:** {signal_color} / {signal_size}  
⏳ **TIME:** {time_frame}  
🔢 **PERIOD:** {period}  
📈 **WIN RATE:** {win_rate}%"""

# 🚀 Start Command
async def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    keyboard = [
        [InlineKeyboardButton("✅ Join WhatsApp Channel", url=WHATSAPP_LINK)],
        [InlineKeyboardButton("🔄 Check & Continue", callback_data="check_join")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"👋 Welcome {user.first_name}!\n\n📌 To continue, please join the WhatsApp channel first:", 
        reply_markup=reply_markup
    )

# 🔄 Check Subscription (Now directly proceeds)
async def check_join(update: Update, context: CallbackContext):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("⚡ Wingo 30 Seconds", callback_data="wingo_30s")],
        [InlineKeyboardButton("⏳ Wingo 1 Minute", callback_data="wingo_1m")],
        [InlineKeyboardButton("⏲️ Wingo 3 Minutes", callback_data="wingo_3m")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text("✅ You have joined WhatsApp!\n\n🎮 Choose a game:", reply_markup=reply_markup)

# 🎮 Handle Wingo Mode Selection & Ask for Period
async def wingo(update: Update, context: CallbackContext):
    query = update.callback_query
    time_frame = ""
    
    if query.data == "wingo_30s":
        time_frame = "30 SEC"
    elif query.data == "wingo_1m":
        time_frame = "1 MIN"
    elif query.data == "wingo_3m":
        time_frame = "3 MIN"

    context.user_data["time_frame"] = time_frame  # Store time frame in user data

    await query.message.reply_text(
        f"""⏱ **MODE SELECTED**  
Time Frame: {time_frame}  
━━━━━━━━━━━━━━  
Enter last 3 digits of period:"""
    )

# 🎯 Receive 3-Digit Period and Generate Signal
async def receive_period(update: Update, context: CallbackContext):
    period = update.message.text.strip()
    
    # ✅ Check if input is exactly 3 digits
    if not period.isdigit() or len(period) != 3:
        await update.message.reply_text("❌ Please enter exactly **3 digits**.")
        return
    
    time_frame = context.user_data.get("time_frame", "Unknown")  # Retrieve time frame

    # Generate Signal
    signal = get_signal(time_frame, period)

    keyboard = [
        [InlineKeyboardButton("NEXT 30 SEC", callback_data="wingo_30s")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(signal, reply_markup=reply_markup)

# 🔥 Main Function
def main():
    app = Application.builder().token(TOKEN).build()

    # ✅ Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_join, pattern="check_join"))
    app.add_handler(CallbackQueryHandler(wingo, pattern="wingo_30s"))
    app.add_handler(CallbackQueryHandler(wingo, pattern="wingo_1m"))
    app.add_handler(CallbackQueryHandler(wingo, pattern="wingo_3m"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_period))

    # 🚀 Start Bot
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
