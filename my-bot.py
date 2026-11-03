from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


TOKEN = "T8890656077:AAGtQySWMjfF0FM9J6TWdViCqPuRZYRiLaE"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello, I am your robot. I will repeat Whatever YOU Want.! 😊')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text 
    await update.message.reply_text(f"You said. : {user_text}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I will repeat Whatever YOU Want /start .')

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))    
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo)) 

    print("The robot is turned on, I'm waiting for a message 🚀")
    app.run_polling() 

if __name__ == '__main__':
    main()
