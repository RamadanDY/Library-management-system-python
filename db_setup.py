import sqlite3
import os
from datetime import datetime

class DatabaseSetup:
    def __init__(self, db_name="library.db"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, db_name)
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Books (
                book_id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                total_copies INTEGER NOT NULL,
                available_copies INTEGER NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                user_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                book_id INTEGER,
                action TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES Users(user_id),
                FOREIGN KEY (book_id) REFERENCES Books(book_id)
            )
        ''')
        self.conn.commit()

    def get_connection(self):
        return self.conn

    def get_cursor(self):
        return self.cursor

    def close(self):
        self.conn.close()