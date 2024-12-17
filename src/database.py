# src/database.py

import sqlite3

class Database:
    def __init__(self, db_name="users.db"):
        """Инициализация базы данных."""
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self._create_table()

    def _create_table(self):
        """Создание таблицы пользователей, если она не существует."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_user_id INTEGER UNIQUE,
                access_token TEXT
            )
        ''')
        self.connection.commit()

    def add_user(self, tg_user_id: int, access_token: str):
        """Добавление нового пользователя в базу данных."""
        try:
            self.cursor.execute('''
                INSERT INTO users (tg_user_id, access_token) VALUES (?, ?)
            ''', (tg_user_id, access_token))
            self.connection.commit()
        except sqlite3.IntegrityError:
            print("Пользователь уже существует.")

    def get_user(self, tg_user_id: int):
        """Получение информации о пользователе по tg_user_id."""
        self.cursor.execute('''
            SELECT * FROM users WHERE tg_user_id = ?
        ''', (tg_user_id,))
        return self.cursor.fetchone()

    def close(self):
        """Закрытие соединения с базой данных."""
        self.connection.close()


