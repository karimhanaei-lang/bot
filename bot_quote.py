import telebot as tl
from base import TOKEN
import app_api

TOKEN = '8890656077:AAGtQySWMjfF0FM9J6TWdViCqPuRZYRiLaE'
bot = tl.TeleBot(TOKEN)


def plot_getter(title: str) -> str:
    plot = app_api.get_movie_info_by_id( \
            app_api.get_movie_info_by_name(title)[4])[5]
    return plot

@bot.message_handler(commands=['start'])
def start(message):
    markup = tl.types.ReplyKeyboardMarkup()

    btn1 = tl.types.KeyboardButton(text='search')
    btn2 = tl.types.KeyboardButton(text='popular')
    btn3 = tl.types.KeyboardButton(text='help')

    markup.add(btn1, btn2, btn3)

    bot.reply_to(message, """🖐👋 Hello and welcome to movie bot API, select a 
    one the commands to continue...""", reply_markup=markup)


@bot.message_handler(commands=['search'])
def search1(message):
    msg = bot.send_message(message.chat.id, '👇 Enter the name of the movie to ' \
    'show details')

    bot.register_next_step_handler(msg, search2)


def search2(message):
    try:
        name = message.text
        result = app_api.get_movie_info_by_name(name)

        markup = tl.types.InlineKeyboardMarkup()

        btn1 = tl.types.InlineKeyboardButton(text='info', \
                                            callback_data=f'info:{result[0]}')
        btn2 = tl.types.InlineKeyboardButton(text='plot', \
                                            callback_data=f'plot:{result[0]}')

        markup.add(btn1, btn2)

        bot.send_message(message.chat.id, '👇 select one of the buttons bellow' \
        ' to show some info', reply_markup=markup)
    except Exception:
        bot.send_message(message.chat.id, '❌ Wrong message or API error...')


@bot.message_handler(commands=['help'])
def helper(message):
    text =  """/start: to start the bot,\n/search: to search for movie,\n/help: to guide,
    \n/popular: to show some popular movies,\nThank you for using this bot."""
    markup = tl.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(commands=['popular'])
def popular(message):
    try:
        popular_list = [app_api.get_movie_info_by_id(i) for i in range(1, 11)]
        text_list = [f'title:{result[0]}, year:{result[1]},' \
                    f'imdb: {result[3]}\n' for result in popular_list]
        text = ''
        for i in text_list:
            text += i
        bot.send_message(message.chat.id, '❤️‍🔥 Here are the 10 most popular movies' \
        f' in imdb:\n{text}')
    except Exception:
        bot.send_message(message.chat.id, '❌ Wrong message or API error...')


@bot.callback_query_handler(func= lambda q: True)
def info_showing(query):
    message_id = query.message.message_id
    try:
        callback, movie_name = query.data.split(':', 1)
        plot = plot_getter(movie_name)
        result = app_api.get_movie_info_by_name(movie_name)
        
        info = f'💬 title:{result[0]} | year:{result[1]} | country:' \
        f'{result[2]} | imdb: {result[3]}'

        if callback == 'plot':
            bot.edit_message_text(message_id=message_id, text=plot)
        else:
            bot.edit_message_text(message_id=message_id, text=info)
    except Exception:
        bot.edit_message_text(message_id=message_id, \
                               text='❌ Wrong message or API error...')


#@bot.message_handler(func= lambda message: True)
#def handle_other_message(message):
#    if message.text == 'return':
#        markup = tl.types.ReplyKeyboardRemove()
#       bot.send_message(message.chat.id, 'let\'s get back to the main menu'
#                         , reply_markup=markup)
#    else:
#        bot.send_message(message.chat.id, 'I can\'t get it can, you say it clearly?')

if __name__ == '__main__':
    bot.infinity_polling()