import os
import dotenv
import telebot
from telebot import types
from main_ex import get_exchange_rate_from_to, get_data

dotenv.load_dotenv()

bot = telebot.TeleBot(os.getenv('TOKEN'))

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, я бот для обмена валют!')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Обменять')
    markup.add(item1)
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Обменять')
def exchange_message(message):
    bot.send_message(message.chat.id, 'Введите код валюты, которую хотите обменять:')
    bot.register_next_step_handler(message, exchange_from_currency)

def exchange_from_currency(message):
    from_currency = message.text.upper()
    bot.send_message(message.chat.id, 'Введите код валюты, которую хотите получить:')
    bot.register_next_step_handler(message, exchange_to_currency, from_currency)

def exchange_to_currency(message, from_currency):
    to_currency = message.text.upper()
    bot.send_message(message.chat.id, 'Введите сумму для обмена:')
    bot.register_next_step_handler(message, exchange_amount, from_currency, to_currency)

def exchange_amount(message, from_currency, to_currency):
    try:
        amount = float(message.text)
    except ValueError:
        bot.send_message(message.chat.id, 'Сумма для обмена должна быть числом. Попробуйте снова.')
        return
    
    converted_amount = get_exchange_rate_from_to(from_currency, to_currency, amount)
    bot.send_message(message.chat.id, f"{amount} {from_currency} = {converted_amount} {to_currency}")

bot.polling()

