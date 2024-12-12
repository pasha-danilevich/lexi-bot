# src/utils.py


def format_message(text: str, format_type: str) -> str:
    switcher = {
        'bold': f"**{text}**",  # Жирный текст
        'spoiler': f"||{text}||",  # Спойлер
        'italic': f"*{text}*",  # Курсив
        'underline': f"__{text}__",  # Подчеркнутый текст
        'strikethrough': f"~~{text}~~",  # Зачеркнутый текст
    }
    
    return switcher.get(format_type, text)  # Возвращает текст без изменений, если формат не найден