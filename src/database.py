# src/database.py

import os
import sqlite3


class Database:
    def __init__(self, db_name="users.db"):
        """Инициализация базы данных."""
        # Получаем путь к директории файла main.py
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # Создаем полный путь к файлу базы данных
        self.db_path = os.path.join(base_dir, db_name)

        print(f"init db")
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self._create_table()

    def _create_table(self):
        """Создание таблицы пользователей, если она не существует."""
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_user_id INTEGER UNIQUE,
                access_token TEXT
            )
        """
        )
        self.connection.commit()

    def add_user(self, tg_user_id: int, access_token: str):
        """Добавление нового пользователя в базу данных."""
        try:
            self.cursor.execute(
                """
                INSERT INTO users (tg_user_id, access_token) VALUES (?, ?)
            """,
                (tg_user_id, access_token),
            )
            self.connection.commit()
        except sqlite3.IntegrityError:
            print("Пользователь уже существует.")

    def get_user(self, tg_user_id: int):
        """Получение информации о пользователе по tg_user_id."""
        self.cursor.execute(
            """
            SELECT * FROM users WHERE tg_user_id = ?
        """,
            (tg_user_id,),
        )
        return self.cursor.fetchone()

    def get_all_users(self):
        """Получение информации о всех пользователях."""
        self.cursor.execute(
            """
            SELECT * FROM users
        """
        )
        return (
            self.cursor.fetchall()
        )  # Используем fetchall для получения всех записей

    def edit_access_token(
        self, tg_user_id: int, new_access_token: str
    ) -> bool:
        """Обновление access_token для указанного пользователя.
        True - Обновлен
        Fasle - Не обновлен
        """
        self.cursor.execute(
            """
            UPDATE users SET access_token = ? WHERE tg_user_id = ?
        """,
            (new_access_token, tg_user_id),
        )
        self.connection.commit()
        # Проверяем количество строк, которые были обновлены
        if self.cursor.rowcount == 0:
            return False
        else:
            return True

        self.connection.commit()

    def close(self):
        """Закрытие соединения с базой данных."""
        self.connection.close()



