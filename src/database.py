# src/database.py

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Пример использования словаря для хранения данных (можно заменить на реальную БД)
users = {}
words = []

def register_user(user_id, username):
    users[user_id] = username

def add_word(word):
    words.append(word)




def get_welcome_message():
    # Создание клавиатуры
    keyboard = InlineKeyboardMarkup(row_width=2)
    register_button = InlineKeyboardButton("Регистрация", callback_data='register')
    login_button = InlineKeyboardButton("Вход", callback_data='login')
    keyboard.add(register_button, login_button)
    
    welcome_text = "Добро пожаловать в lexi бот! Бот для удобного изучения английского."
    
    return welcome_text, keyboard