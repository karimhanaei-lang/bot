import logging
import requests
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# --- تنظیمات ---
BOT_TOKEN = "YOUR_BOT_TOKEN"
WEATHER_API_KEY = "YOUR_WEATHER_API_KEY"

logging.basicConfig(level=logging.INFO)

def fetch_weather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"API Error: {e}")
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # شرط ۱: Reply Keyboard
    keyboard = [["🌤 Search Weather"], ["❓ Help"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Welcome to Weather Bot! ☁️\nChoose an option:", reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🌤 Search Weather":
        # شرط ۲: Keyboard Removal
        await update.message.reply_text("Please enter the city name:", reply_markup=ReplyKeyboardRemove())
        context.user_data['state'] = 'GETTING_CITY'
    
    elif text == "❓ Help":
        # شرط ۴: Keyboard Removal
        await update.message.reply_text("Instructions: Enter the city name after clicking Search to see the weather.", reply_markup=ReplyKeyboardRemove())
    
    elif context.user_data.get('state') == 'GETTING_CITY':
        # شرط ۵: Error Handling
        data = fetch_weather(text)
        if data:
            # شرط ۳: Inline Keyboard برای نمایش جزئیات
            keyboard = [[InlineKeyboardButton("View Full Details 📊", callback_data=f"city_{text}")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(f"Weather in {text}: {data['weather'][0]['description']}, {data['main']['temp']}°C", reply_markup=reply_markup)
        else:
            await update.message.reply_text("City not found or API error. Please check the spelling.")
        context.user_data['state'] = None

async def weather_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    city = query.data.split('_')[1]
    
    data = fetch_weather(city)
    if data:
        detail_text = (f"📊 *Full Weather Report for {city}:*\n\n"
                       f"🌡 Temp: {data['main']['temp']}°C\n"
                       f"💧 Humidity: {data['main']['humidity']}%\n"
                       f"💨 Wind: {data['wind']['speed']} m/s\n"
                       f"☁️ Condition: {data['weather'][0]['description']}")
        await query.edit_message_text(text=detail_text, parse_mode='Markdown')

if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(weather_details))
    app.run_polling()