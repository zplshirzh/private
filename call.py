from telebot import types

import telebot
token='7492612967:AAExbOQ1Dz_vLT_UBCMx_T5sogAGlPdbU5s'
TO_CHAT_ID =7764132164

bot = telebot.TeleBot(token)

requests_queue = []


@bot.message_handler(commands=['start'])
def welcome(message):
    markup=types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button1=types.KeyboardButton('Тарифы $')
    
    markup.add(button1)
    bot.send_message(message.chat.id,
                     "Ознакомься с тарифами,\nэто можно сделать по кнопке ниже👇 ".format(message.from_user, bot.get_me()),parse_mode='html',reply_markup=markup)
@bot.message_handler(content_types=['text','photo'])
def message_reply(message):    
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    week=types.KeyboardButton('Неделя')
    month=types.KeyboardButton('Месяц')
    always=types.KeyboardButton('Навсегда')
    pay=types.KeyboardButton('Я оплатил')
    
    user_id=message.from_user.id
    
    
    markup.add(week,month,always)
    if message.text=='Тарифы $':
        
        
        bot.send_message(message.chat.id,'Чтобы ознакомиться с тарифом, выбери необходимый, нажав соответствующую кнопку',reply_markup=markup)
        
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    delete.markup()
    markup.add(pay)
    
    

    if message.text=='Неделя':
                
                     
            bot.send_message(user_id,"Способ оплаты:\nПо номеру +7 (915) 785 16 13 Федор Г. \nТ-Банк(Обязательно!)\n  \nК оплате: 160.00 🇷🇺RUB",reply_markup=markup)
                
    if message.text=='Месяц':
                
            bot.send_message(message.chat.id,"Способ оплаты:\nПо номеру +7 (915) 785 16 13 Федор Г. \nТ-Банк(Обязательно!)\n  \nК оплате: 380.00 🇷🇺RUB",reply_markup=markup)
    if message.text=='Навсегда':
                
            bot.send_message(message.chat.id,"Способ оплаты:\nПо номеру +7 (915) 785 16 13 Федор Г. \nТ-Банк(Обязательно!)\n  \nК оплате: 960.00 🇷🇺RUB",reply_markup=markup)
        
    if message.text=='Я оплатил':
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id,"Отправь скриншот об оплате ",reply_markup=markup)
        bot.register_next_step_handler(message, help_bot)
    
        


# Функция, отправляющая вопрос от пользователя в чат поддержки
def help_bot(message):
    requests_queue.append((message.message_id, message.chat.id))
    bot.forward_message(TO_CHAT_ID, message.chat.id, message.message_id)
    markup_inline = types.InlineKeyboardMarkup([[
        types.InlineKeyboardButton(text='Ответить', callback_data=f'answer{message.chat.id}')
    ]])
    bot.send_message(TO_CHAT_ID, f"Действие:", reply_markup=markup_inline)
    


@bot.message_handler(commands=["requests"], func=lambda m: int(m.chat.id) == int(TO_CHAT_ID))
def all_messages(message):
    bot.send_message(message.chat.id, "Доступные запросы:")
    for i, req in enumerate(requests_queue):
        bot.forward_message(TO_CHAT_ID, req[1], req[0])
        markup_inline = types.InlineKeyboardMarkup([[
            types.InlineKeyboardButton(text='Ответить', callback_data=f'answer{req[1]}')
        ]])
        bot.send_message(message.chat.id, f"Действие:", reply_markup=markup_inline)


def send_answer(message: types.Message, call, chat_id):
    markup_inline = types.InlineKeyboardMarkup()
    btn_my_site = types.InlineKeyboardButton(text='Приват', url='https://t.me/+HJFaNfQ3QLowZGE6')
    markup_inline.add(btn_my_site)
    if message.text == 'yes':
        markup = types.ReplyKeyboardRemove()
        bot.send_message(call.message.chat.id, "Ответ отправлен!",reply_markup=markup)
        bot.send_message(chat_id, "Нажимай на кнопку ниже",reply_markup=markup_inline)
        for i, req in enumerate(requests_queue):
            if int(req[1]) == int(chat_id):
                del requests_queue[i]
    elif message.text == 'no':
        markup = types.ReplyKeyboardRemove()
        bot.send_message(call.message.chat.id, "Ответ отправлен!",reply_markup=markup)
        bot.send_message(chat_id, "Что-то пошло не так :(")
        


@bot.callback_query_handler(func=lambda call: True)
def answer_callback(call: types.CallbackQuery):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    yes = types.KeyboardButton(text='yes')
    no = types.KeyboardButton(text='no')
    markup.add(yes,no)
    if call.data.startswith("answer"):
        
        
        chat_id = int(call.data[6:])

        bot.send_message(call.message.chat.id, "Отправьте ответ на запрос",reply_markup=markup)
        bot.register_next_step_handler(call.message, lambda msg: send_answer(msg, call, chat_id))


bot.polling(none_stop=True)
