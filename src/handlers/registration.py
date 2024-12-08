# src/handlers/registration.py

def registration_handler(bot, message):
    bot.send_message(message.chat.id, "Введите ваше имя для регистрации:")
    # Логика обработки имени пользователя может быть добавлена здесь.