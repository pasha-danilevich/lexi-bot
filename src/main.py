# src/main.py

from config import TG_TOKEN
import telebot
from handler import BotHandlers

if __name__ == '__main__':
    bot = telebot.TeleBot(TG_TOKEN)
    
    # Создаем экземпляр класса BotHandlers и передаем бота
    handlers = BotHandlers(bot)  # Передаем объект TeleBot
    print('is working...')
    bot.polling(none_stop=True)