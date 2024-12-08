# src/handlers/welcome.py

from database import get_welcome_message

def welcome_handler(bot, message):
    welcome_message, keyboard = get_welcome_message()
    bot.send_message(message.chat.id, welcome_message, reply_markup=keyboard)