import json
from telebot import TeleBot
from telebot.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
import requests
from config import DOMAIN
from handlers.login import login_handler
from user import User
from utils import escape_markdown_v2, format_message

API_URL = f'http://{DOMAIN}/api/auth/users/'

# Глобальный объект пользователя
current_user = User(email='', username='', password='')

def registration_handler(bot: TeleBot, message: Message):
    global current_user  # Используем глобальный объект пользователя
    bot.send_message(message.chat.id, "Введите ваш email:")
    bot.register_next_step_handler(message, process_email, bot)

def process_email(message: Message, bot: TeleBot):
    global current_user  # Используем глобальный объект пользователя
    
    if message.text:
        current_user.email = message.text.strip()
    
    bot.send_message(message.chat.id, "Введите ваш username:")
    bot.register_next_step_handler(message, process_username, bot)

def process_username(message: Message, bot: TeleBot):
    global current_user  # Используем глобальный объект пользователя
    
    if message.text:
        current_user.username = message.text.strip() 
    bot.send_message(message.chat.id, "Введите ваш пароль (убедитесь, что его никто не видит):")
    bot.register_next_step_handler(message, process_password, bot)

def process_password(message: Message, bot: TeleBot):
    global current_user  # Используем глобальный объект пользователя
    
    if message.text:
        current_user.password = message.text.strip() 
    bot.send_message(message.chat.id, "Введите ваш пароль еще раз:")
    bot.register_next_step_handler(message, confirm_password, bot)

def confirm_password(message: Message, bot: TeleBot):
    global current_user  # Используем глобальный объект пользователя
    
    if message.text:
        re_password = message.text.strip()

    if current_user.password != re_password:
        bot.send_message(message.chat.id, "Пароли не совпадают. Попробуйте снова.")
        return registration_handler(bot, message)  # Начинаем регистрацию заново

    # Создаем клавиатуру с кнопками подтверждения и повторной регистрации
    buttons = get_confirm_buttons()
    
    # Формируем текст для подтверждения
    text1 = f'Вы ввели следующие данные: \nEmail: {current_user.email} \nUsername: {current_user.username} '
    text2 = f'\nPassword: {format_message(escape_markdown_v2(current_user.password), "spoiler")}'
    
    escaped_text = escape_markdown_v2(text1) + text2
    print(escaped_text)
    # Отправляем сообщение с данными и кнопками
    bot.send_message(
        message.chat.id,
        text=escaped_text,
        reply_markup=buttons,
        parse_mode='MarkdownV2'
    )

def get_confirm_buttons():
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    # Кнопка подтверждения без передачи данных через callback_data
    confirm_button = InlineKeyboardButton(text="Подтвердить", callback_data='confirm')
    
    register_button = InlineKeyboardButton(text="Заново", callback_data='register')
    
    keyboard.add(confirm_button, register_button)
    
    return keyboard

# Обработчик нажатий кнопок подтверждения и повторной регистрации
def handle_confirmation(bot: TeleBot, call: CallbackQuery):
    global current_user  # Используем глобальный объект пользователя
    
    payload = {
        "email": current_user.email,
        "username": current_user.username,
        "password": current_user.password,
        "re_password": current_user.password  # Используем тот же пароль для повторного ввода
    }
    bot.send_message(call.message.chat.id, "Думаю...")
    # Выполняем POST-запрос к API
    response = requests.post(API_URL, json=payload)

    if response.status_code == 201:
        bot.send_message(call.message.chat.id, "Регистрация прошла успешно! \nТеперь надо войти в аккаунт.")
        return login_handler(bot=bot, message=call.message)  # type: ignore # Вход в аккаунт
    else:
        error_message = response.json().get('detail', 'Ошибка при регистрации.')
        buttons = get_buttons()
        bot.send_message(call.message.chat.id, f"Ошибка при регистрации: {error_message}.", reply_markup=buttons)

# Регистрация обработчика callback_query_handler
def register_handlers(bot: TeleBot):
    @bot.callback_query_handler(func=lambda call: call.data == 'confirm')
    def confirmation_handler(call):
        handle_confirmation(bot=bot, call=call)

def get_buttons():
    keyboard = InlineKeyboardMarkup(row_width=2)
    register_button = InlineKeyboardButton("Попробовать еще раз", callback_data='register')
    login_button = InlineKeyboardButton("Вход", callback_data='login')
    keyboard.add(register_button, login_button)
    
    return keyboard
