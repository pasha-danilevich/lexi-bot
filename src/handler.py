# src/handler.py

import telebot
from handlers.welcome import welcome_handler
from handlers.registration import registration_handler
from handlers.login import login_handler

class BotHandlers:
    def __init__(self, bot: telebot.TeleBot):
        self.bot = bot
        
        # Регистрация обработчиков команд
        self.register_handlers()

    def register_handlers(self):
        self.bot.message_handler(commands=['start'])(self.start_handler)
        self.bot.callback_query_handler(func=lambda call: True)(self.callback_query_handler)

    def start_handler(self, message: telebot.types.Message):
        welcome_handler(self.bot, message)

    def callback_query_handler(self, call: telebot.types.CallbackQuery):
        # Обработка нажатий на кнопки
        if call.data == 'register':
            registration_handler(self.bot, call.message)
        elif call.data == 'login':
            login_handler(self.bot, call.message)