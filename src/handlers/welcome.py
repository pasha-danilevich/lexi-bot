# src/handlers/welcome.py

from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def send_welcome(bot: TeleBot, message):
    welcome_message = get_welcome_message()
    buttons = get_buttons()
    bot.send_message(message.chat.id, welcome_message, reply_markup=buttons)
    
def get_welcome_message():
    welcome_text = "Добро пожаловать в lexi бот! Бот для удобного изучения английского."
    
    return welcome_text

def get_buttons():
    # Создание клавиатуры
    keyboard = InlineKeyboardMarkup(row_width=2)
    register_button = InlineKeyboardButton("Регистрация", callback_data='register')
    login_button = InlineKeyboardButton("Вход", callback_data='login')
    keyboard.add(register_button, login_button)
    
    return keyboard