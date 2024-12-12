# src/main.py

from config import TG_TOKEN
import telebot
from handler import register_handlers

def main():
    bot = telebot.TeleBot(TG_TOKEN)

    # Регистрация обработчиков команд
    register_handlers(bot)

    print('Бот запущен и работает...')
    bot.polling(none_stop=True)

if __name__ == '__main__':
    main()
