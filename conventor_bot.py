import os
import telebot
from currency_converter import CurrencyConverter
from telebot import types
from dotenv import load_dotenv


load_dotenv()

token = os.getenv('TOKEN')

bot = telebot.TeleBot(token)
currency = CurrencyConverter()
amount = 0

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Введите сумму')
    bot.register_next_step_handler(message, summa)

def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, "Введите значение в виде числа" )
        bot.register_next_step_handler(message, summa()) #вписываем эту же функцию как следующее действие
        return
    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('USD/GBP', callback_data='usd/gbp')
        btn4 = types.InlineKeyboardButton('Другой вариант', callback_data='else')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, "Выберите вариант ковертации", reply_markup=markup)
    elif amount == 0:
        bot.send_message(message.chat.id, 'Ноль, он в любой валюте ноль. Введите число больше нуля.')
        bot.register_next_step_handler(message, summa)
    else:
        bot.send_message(message.chat.id, 'Отрицательное число? ну-ну. Введите число больше нуля.')
        bot.register_next_step_handler(message, summa)

#метод обработки callback_data
@bot.callback_query_handler( func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Получается {round(res, 2)}. Можете вписать другую сумму. ')
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, 'ВВедите нужные валюты на латинице через слеш(/).' )
        bot.register_next_step_handler(call.message, my_currency)

def my_currency (message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Получается {round(res, 2)}. Можете вписать другую сумму. ')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, f'Что-то пошло не по плану. Введите нужные валюты на латинице через слеш(/)!')
        bot.register_next_step_handler(message, summa)


bot.polling(none_stop=True)