
import telebot
from telebot import types
import requests 

TOKEN = '8890656077:AAGtQySWMjfF0FM9J6TWdViCqPuRZYRiLaE'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔍 Search Topic", "🎲 Random Quote", "❓ Help")
    bot.send_message(message.chat.id, "Welcome to Quotes Bot! 📚\nChoose an option:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "🔍 Search Topic":
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Enter a topic (e.g., wisdom, love, film):", reply_markup=markup)
        bot.register_next_step_handler(message, process_topic)
    
    elif message.text == "🎲 Random Quote":
        send_api_quote(message, topic=None)

    elif message.text == "❓ Help":
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Use the buttons to get quotes!", reply_markup=markup)

def process_topic(message):
    topic = message.text.lower()
    send_api_quote(message, topic)

def send_api_quote(message, topic=None):
    try:
        url = "https://api.quotable.io/random"
        if topic:
            url += f"?tags={topic}"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Show Author ✍️", callback_data=f"auth_{data['author']}"))
            
            text = f"✨ *Quote:*\n\n\"{data['content']}\""
            bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Topic not found. Try 'wisdom' or 'love'.")
            
    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Error connecting to API. Please check your VPN!")

@bot.callback_query_handler(func=lambda call: call.data.startswith('auth_'))
def show_author(call):
    author = call.data.split('_')[1]
    bot.answer_callback_query(call.id, f"Author: {author}")
    bot.send_message(call.message.chat.id, f"✍️ This quote was written by: *{author}*", parse_mode='Markdown')

if __name__ == '__main__':
    print("Quotes Bot is running with REAL API...")
    bot.polling(non_stop=True)