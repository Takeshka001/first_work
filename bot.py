import os
import dotenv
import telebot
from telebot import types
from main import get_forecast, get_and_format_weekly_forecast

dotenv.load_dotenv()

bot = telebot.TeleBot(os.getenv('TOKEN'))

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет, я бот для получения прогноза погоды. Введи название города:")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    data = get_and_format_weekly_forecast(message.text)
    if data is None:
        bot.send_message(message.chat.id, "Город не найден. Попробуйте еще раз.")   
    else:
        for day in data:
            bot.send_message(message.chat.id, day)

if __name__ == '__main__':
    bot.polling(none_stop=True)