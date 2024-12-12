# src/handler.py

from telebot import TeleBot
from telebot.types import Message
from handlers import login, registration, welcome

def register_handlers(bot: TeleBot):
    # Обработчик первого входа
    @bot.message_handler(commands=['start'])
    def start_command(message: Message):
        welcome.send_welcome(bot, message)

    # Обработчики для логина и регистрации
    @bot.callback_query_handler(func=lambda call: call.data == 'register')
    def register_command(call):
        registration.registration_handler(bot, call.message)

    @bot.callback_query_handler(func=lambda call: call.data == 'login')
    def login_command(call):
        login.login_handler(bot, call.message)

    @bot.message_handler(func=lambda message: True)
    def echo_all(message: Message):
        bot.reply_to(message, f'{message.text}? Не знаю такой команды')
