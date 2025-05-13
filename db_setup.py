import sqlite3
import os

class DatabaseSetup:
    """A class to initialize the SQLite database schema."""
    
    def __init__(self, db_name: str = "library.db"):
        """
        Initialize the database and create tables.
        
        Args:
            db_name (str): Name of the SQLite database file.
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, db_name)
        self.create_tables()

    def create_tables(self) -> None:
        """
        Create the necessary tables in the database if they don't exist.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Books (
            book_id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            total_copies INTEGER NOT NULL,
            available_copies INTEGER DEFAULT 0
        )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                user_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                book_id INTEGER,
                action TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES Users(user_id),
                FOREIGN KEY (book_id) REFERENCES Books(book_id)
            )
        """)
        
        conn.commit()
        conn.close()

    def get_db_path(self) -> str:
        """
        Get the path to the database file.
        
        Returns:
            str: Path to the SQLite database file.
        """
        return self.db_path