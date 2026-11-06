import telebot
import base

bot  = telebot.TeleBot(base.TOKEN)
print('bot created ....')

url_photo_online = 'https://picsum.photos/600/400'

@bot.message_handler(commands=['media'])
def show_media_menu(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    local_photo_btn = telebot.types.InlineKeyboardButton(text='Local Photo Upload',
                                           callback_data='local_photo')
    local_document_btn = telebot.types.InlineKeyboardButton(text='Local document Upload',
                                            callback_data='local_doc')
    online_photo_btn = telebot.types.InlineKeyboardButton(text='Online Photo Upload',
                                            callback_data='online_photo')

    markup.add(local_photo_btn, local_document_btn, online_photo_btn)
    bot.send_message(message.chat.id , text='یکی از گرینه ها را انتخاب کنید ', reply_markup=markup)

@bot.callback_query_handler(func=lambda call:True)
def manage_call(call):
    call_id = call.message.chat.id

    if call.data == 'local_photo':
        with open('./media/IMG_0036.jpg', 'rb') as f:
            bot.send_photo(call_id, f)

    if call.data == 'online_photo':
        bot.send_photo(call_id, photo=url_photo_online , caption='تصویر آنلاین')

    if call.data == 'local_doc':
        with open('./media/doc.pdf', 'rb') as f:
            bot.send_document(call_id, f)


if __name__ == '__main__':
    bot.infinity_polling()