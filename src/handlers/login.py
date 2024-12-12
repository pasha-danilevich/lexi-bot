# src/handlers/login.py

from requests import status_codes
from telebot import TeleBot
import requests
from config import DOMAIN
from handlers.welcome import get_buttons

# Формируем URL для API
API_URL = f'http://{DOMAIN}/api/jwt/create/'

def login_handler(bot: TeleBot, message):
    bot.send_message(message.chat.id, "Введите ваш username или почту:")
    bot.register_next_step_handler(message, process_username, bot)

def process_username(message, bot: TeleBot):
    username = message.text.strip()
    bot.send_message(message.chat.id, "Введите ваш пароль:")
    bot.register_next_step_handler(message, process_password, username, bot)

def process_password(message, username: str, bot: TeleBot):
    password = message.text.strip()
    
    # Выполняем POST-запрос к API
    bot.send_message(message.chat.id, "Думаю...")
    
    response = requests.post(API_URL, json={"username": username, "password": password})

    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens.get("access")
        refresh_token = tokens.get("refresh")

        bot.send_message(message.chat.id, f"Вход выполнен успешно!\nAccess Token: {access_token[:5]}\nRefresh Token: {refresh_token[:5]}")
    elif response.status_code == 401:
        text = "Ошибка при входе. Проверьте свои введенные данные данные."
        buttons = get_buttons()
        bot.send_message(message.chat.id, text, reply_markup=buttons)
    else:
        bot.send_message(message.chat.id, "Произошла неожиданная ошибка, повторите попытку позже.")
