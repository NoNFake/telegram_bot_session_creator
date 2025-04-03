# SQL save user ID
import sqlite3
import os
from typing import List, Tuple


class TelegramUserDatabase:
    """Клас для керування користувачами Telegram та їхніми сесіями в базі даних."""
    
    def __init__(self, db_path: str = "telegram_users.db"):
        """Ініціалізація підключення до бази даних."""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self._connect()
        self._create_tables()
        self._migrate_database() 

    def _connect(self):
        """Підключення до бази даних."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Помилка підключення до бази даних: {e}")
            raise
    
    def _create_tables(self):
        """Створення необхідних таблиць, якщо вони не існують."""
        try:
            # Таблиця користувачів
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    language TEXT DEFAULT NULL
                )
            ''')
            
            # Таблиця сесій
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    session_name TEXT NOT NULL,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    session_data TEXT,
                    password TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''')
            
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Помилка створення таблиць: {e}")
            self.conn.rollback()
            raise
    
    def _migrate_database(self):
        """Міграція бази даних для додавання нових колонок."""
        try:
            # Перевірка наявності колонки password в таблиці sessions
            self.cursor.execute("PRAGMA table_info(sessions)")
            columns = [column[1] for column in self.cursor.fetchall()]
            
            if "password" not in columns:
                # print("Додавання колонки password до таблиці sessions...")
                self.cursor.execute("ALTER TABLE sessions ADD COLUMN password TEXT")
                self.conn.commit()
                print("Міграцію успішно виконано.")
            
        except sqlite3.Error as e:
            print(f"Помилка при міграції бази даних: {e}")
            self.conn.rollback()


    """ Users """
    def save_user(self, user_id: int, username: str = None, first_name: str = None, last_name: str = None, language: str = None) -> bool:
        """
        Зберегти або оновити інформацію про користувача в базі даних.
        
        Args:
            user_id: ID користувача Telegram
            username: Ім'я користувача Telegram
            first_name: Ім'я користувача
            last_name: Прізвище користувача
            language: Мова користувача
            
        Returns:
            bool: True, якщо успішно, False в іншому випадку
        """
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO users (user_id, username, first_name, last_name, language)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, username, first_name, last_name, language))
            
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Помилка збереження користувача: {e}")
            self.conn.rollback()
            return False
        
    def set_user_language(self, user_id: int, language: str) -> bool:
        """
        Встановити мову для користувача.
        
        Args:
            user_id: ID користувача Telegram
            language: Код мови (наприклад, 'uk', 'en')
            
        Returns:
            bool: True, якщо успішно, False в іншому випадку
        """
        try:
            self.cursor.execute('''
                UPDATE users 
                SET language = ? 
                WHERE user_id = ?
            ''', (language, user_id))
            
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Помилка встановлення мови: {e}")
            self.conn.rollback()
            return False

    def get_user_language(self, user_id: int) -> str:
        """
        Отримати мову користувача.
        
        Args:
            user_id: ID користувача Telegram
            
        Returns:
            str: Код мови або None, якщо не встановлено
        """
        try:
            self.cursor.execute('''
                SELECT language
                FROM users
                WHERE user_id = ?
            ''', (user_id,))
            
            result = self.cursor.fetchone()
            if result:
                return result[0]
            return None
        except sqlite3.Error as e:
            print(f"Помилка отримання мови: {e}")
            return None




    """ Sessions """
    def save_session(self, user_id: int, session_name: str, session_data: str, password: str = None) -> bool:
        """
        Зберегти нову сесію для користувача.
        
        Args:
            user_id: ID користувача Telegram
            session_name: Назва сесії
            session_data: Дані сесії
            
        Returns:
            bool: True, якщо успішно, False в іншому випадку
        """
        try:
            # Перевірка наявності користувача
            self.cursor.execute('SELECT 1 FROM users WHERE user_id = ?', (user_id,))
            if not self.cursor.fetchone():
                print(f"Користувач {user_id} не знайдений. Неможливо зберегти сесію.")
                return False
            
            self.cursor.execute('''
                INSERT INTO sessions (user_id, session_name, session_data, password)
                VALUES (?, ?, ?, ?)
            ''', (user_id, session_name, session_data, password))
            
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Помилка збереження сесії: {e}")
            self.conn.rollback()
            return False
    
    def get_user_sessions(self, user_id: int) -> List[Tuple[str, str]]:
        """
        Отримати всі сесії користувача.
        
        Args:
            user_id: ID користувача Telegram
            
        Returns:
            Список кортежів, що містять (session_name, session_data)
        """
        try:
            self.cursor.execute('''
                SELECT session_name, session_data
                FROM sessions
                WHERE user_id = ?
                ORDER BY created_date DESC
            ''', (user_id,))
            
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Помилка отримання сесій: {e}")
            return []
    
    def count_user_sessions(self, user_id: int) -> int:
        """
        Підрахувати кількість сесій, створених користувачем.
        
        Args:
            user_id: ID користувача Telegram
            
        Returns:
            int: Кількість сесій
        """
        try:
            self.cursor.execute('''
                SELECT COUNT(*)
                FROM sessions
                WHERE user_id = ?
            ''', (user_id,))
            
            return self.cursor.fetchone()[0]
        except sqlite3.Error as e:
            print(f"Помилка підрахунку сесій: {e}")
            return 0
    
    def close(self):
        """Закрити з'єднання з базою даних."""
        if self.conn:
            self.conn.close()
            
    def __del__(self):
        """Деструктор для гарантованого закриття з'єднання з базою даних."""
        self.close()