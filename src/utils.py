# src/utils.py


from aiogram.types import Message

from database import Database, User


def format_message(text: str, format_type: str) -> str:
    switcher = {
        'bold': f"**{text}**",  # Жирный текст
        'spoiler': f"||{text}||",  # Спойлер
        'italic': f"*{text}*",  # Курсив
        'underline': f"__{text}__",  # Подчеркнутый текст
        'strikethrough': f"~~{text}~~",  # Зачеркнутый текст
    }
    
    return switcher.get(format_type, text)  # Возвращает текст без изменений, если формат не найден


def escape_markdown_v2(text):
    """ Экранирует специальные символы для MarkdownV2. """
    escape_chars = r'_ * [ ] ( ) ~ ` > # + - = | { } . !'.split()
    for char in escape_chars:
        text = text.replace(char, f'\\{char}')
    return text


async def get_user(message: Message, db: Database) -> User | None:
    if message.from_user:
        user_id = message.from_user.id
        
    user_data = db.get_user(tg_user_id=user_id)

    if user_data:
        user = User(user_data=user_data )
    else:
        user = None
    
    return user