import telebot
from telebot import types
import random

TOKEN = '8890656077:AAGtQySWMjfF0FM9J6TWdViCqPuRZYRiLaE'
bot = telebot.TeleBot(TOKEN)

QUOTES_DATABASE = {
    "general": [
        {"content": "The only way to do great work is to love what you do.", "author": "Steve Jobs"},
        {"content": "Believe you can and you're halfway there.", "author": "Theodore Roosevelt"},
        {"content": "It always seems impossible until it's done.", "author": "Nelson Mandela"},
        {"content": "Stay hungry, stay foolish.", "author": "Steve Jobs"},
    ],
    "wisdom": [
        {"content": "The more that you read, the more things you will know.", "author": "Dr. Seuss"},
        {"content": "Knowledge is power.", "author": "Francis Bacon"},
        {"content": "The only true wisdom is in knowing you know nothing.", "author": "Socrates"},
    ],
    "love": [
        {"content": "Love all, trust a few, do wrong to none.", "author": "William Shakespeare"},
        {"content": "Where there is love there is life.", "author": "Mahatma Gandhi"},
    ]
}

def get_random_quote():
    return random.choice(QUOTES_DATABASE["general"])

def get_quote_by_topic(topic):
    topic = topic.lower()
    if topic in QUOTES_DATABASE:
        return random.choice(QUOTES_DATABASE[topic])
    else:
        return random.choice(QUOTES_DATABASE["general"])

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🎲 جمله تصادفی", "🔍 جستجوی موضوع")
    markup.add("❓ راهنما")
    bot.send_message(message.chat.id, "سلام! به ربات جملات قصار خوش آمدید. 📚\nیک گزینه را انتخاب کنید:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_options(message):
    if message.text.startswith('/'): return

    if message.text == "🎲 جمله تصادفی":
        data = get_random_quote()
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("درباره نویسنده ✍️", callbackdata=f"auth_{data['author']}")
        markup.add(btn)
        text = f"✨ جمله روز:\n\n\"{data['content']}\"\n\n— {data['author']}"
        bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=markup)

    elif message.text == "🔍 جستجوی موضوع":
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "لطفاً یک موضوع را وارد کنید (مثلاً: wisdom, love):", reply_markup=markup)
        bot.register_next_step_handler(message, process_topic)

    elif message.text == "❓ راهنما":
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "شما می‌توانید جملات تصادفی بگیرید یا بر اساس موضوع جستجو کنید.", reply_markup=markup)
        main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        main_menu.add("🎲 جمله تصادفی", "🔍 جستجوی موضوع", "❓ راهنما")
        bot.send_message(message.chat.id, "منوی اصلی بازگردانده شد. ✅", reply_markup=main_menu)

def process_topic(message):
    topic = message.text.lower()
    data = get_quote_by_topic(topic)

    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("درباره نویسنده ✍️", callbackdata=f"auth_{data['author']}")
    markup.add(btn)

    text = f"🔎 نتیجه برای موضوع {topic}:\n\n\"{data['content']}\"\n\n— {data['author']}"
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=markup)

    main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_menu.add("🎲 جمله تصادفی", "🔍 جستجوی موضوع", "❓ راهنما")
    bot.send_message(message.chat.id, "بازگشت به منوی اصلی...", reply_markup=main_menu)

@bot.callback_query_handler(func=lambda call: call.data.startswith('auth_'))
def author_callback(call):
    author_name = call.data.split('_')[1]
    bot.answer_callback_query(call.id, f"نویسنده این اثر: {author_name} است. 🌟")

if __name__ == '__main__':
    print("Bot is running successfully! (Offline Mode enabled)")
    bot.polling(non_stop=True)