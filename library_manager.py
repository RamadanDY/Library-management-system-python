import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Tuple

class Library:
    """A class to manage library operations using an SQLite database."""
    
    def __init__(self, conn: sqlite3.Connection):
        """
        Initialize the Library with a database connection.
        
        Args:
            conn (sqlite3.Connection): SQLite database connection.
        """
        self.conn = conn
        self.cursor = conn.cursor()

    def add_book(self, book_id: int, title: str, author: str, total_copies: int) -> Tuple[bool, str]:
        """
        Add a book to the library.
        
        Args:
            book_id (int): Unique identifier for the book.
            title (str): Title of the book.
            author (str): Author of the book.
            total_copies (int): Total number of copies.
            
        Returns:
            Tuple[bool, str]: (Success status, Error message if any).
        """
        if not all([isinstance(book_id, int), isinstance(total_copies, int)]):
            return False, "Book ID and total copies must be integers"
        if total_copies < 1:
            return False, "Total copies must be positive"
        if not title or not author:
            return False, "Title and author must not be empty"
            
        try:
            self.cursor.execute("SELECT book_id FROM Books WHERE book_id = ?", (book_id,))
            if self.cursor.fetchone():
                return False, f"Book ID {book_id} already exists"
                
            self.cursor.execute(
                """
                INSERT INTO Books (book_id, title, author, total_copies, available_copies)
                VALUES (?, ?, ?, ?, ?)
                """,
                (book_id, title, author, total_copies, total_copies)
            )
            self.conn.commit()
            return True, ""
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"

    def register_user(self, user_id: int, name: str) -> Tuple[bool, str]:
        """
        Register a new user.
        
        Args:
            user_id (int): Unique identifier for the user.
            name (str): Name of the user.
            
        Returns:
            Tuple[bool, str]: (Success status, Error message if any).
        """
        if not isinstance(user_id, int):
            return False, "User ID must be an integer"
        if not name:
            return False, "Name must not be empty"
            
        try:
            self.cursor.execute("SELECT user_id FROM Users WHERE user_id = ?", (user_id,))
            if self.cursor.fetchone():
                return False, f"User ID {user_id} already exists"
                
            self.cursor.execute(
                "INSERT INTO Users (user_id, name) VALUES (?, ?)",
                (user_id, name)
            )
            self.conn.commit()
            return True, ""
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"

    def borrow_book(self, user_id: int, book_id: int) -> Tuple[bool, str]:
        """
        Borrow a book for a user.
        
        Args:
            user_id (int): ID of the user.
            book_id (int): ID of the book.
            
        Returns:
            Tuple[bool, str]: (Success status, Error message if any).
        """
        if not all([isinstance(user_id, int), isinstance(book_id, int)]):
            return False, "User ID and Book ID must be integers"
            
        try:
            # Check if user exists
            self.cursor.execute("SELECT user_id FROM Users WHERE user_id = ?", (user_id,))
            if not self.cursor.fetchone():
                return False, f"User ID {user_id} not found"
                
            # Check if book exists and has available copies
            self.cursor.execute(
                "SELECT book_id, available_copies, title FROM Books WHERE book_id = ?",
                (book_id,)
            )
            book = self.cursor.fetchone()
            if not book:
                return False, f"Book ID {book_id} not found"
            if book[1] <= 0:
                return False, f"No copies of '{book[2]}' available"
                
            # Check if user already borrowed the book
            self.cursor.execute(
                """
                SELECT t.book_id FROM Transactions t
                WHERE t.user_id = ? AND t.book_id = ? AND t.action = 'borrow'
                AND NOT EXISTS (
                    SELECT 1 FROM Transactions t2
                    WHERE t2.user_id = t.user_id AND t2.book_id = t.book_id AND t2.action = 'return'
                    AND t2.timestamp > t.timestamp
                )
                """,
                (user_id, book_id)
            )
            if self.cursor.fetchone():
                return False, f"User already borrowed '{book[2]}'"
                
            # Update available copies and record transaction
            self.cursor.execute(
                "UPDATE Books SET available_copies = available_copies - 1 WHERE book_id = ?",
                (book_id,)
            )
            self.cursor.execute(
                """
                INSERT INTO Transactions (user_id, book_id, action, timestamp)
                VALUES (?, ?, 'borrow', ?)
                """,
                (user_id, book_id, datetime.now().isoformat())
            )
            self.conn.commit()
            return True, ""
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"

    def return_book(self, user_id: int, book_id: int) -> Tuple[bool, str]:
        """
        Return a book borrowed by a user.
        
        Args:
            user_id (int): ID of the user.
            book_id (int): ID of the book.
            
        Returns:
            Tuple[bool, str]: (Success status, Error message if any).
        """
        if not all([isinstance(user_id, int), isinstance(book_id, int)]):
            return False, "User ID and Book ID must be integers"
            
        try:
            # Check if user exists
            self.cursor.execute("SELECT user_id FROM Users WHERE user_id = ?", (user_id,))
            if not self.cursor.fetchone():
                return False, f"User ID {user_id} not found"
                
            # Check if book exists
            self.cursor.execute(
                "SELECT book_id, title FROM Books WHERE book_id = ?",
                (book_id,)
            )
            book = self.cursor.fetchone()
            if not book:
                return False, f"Book ID {book_id} not found"
                
            # Check if user borrowed the book
            self.cursor.execute(
                """
                SELECT t.book_id FROM Transactions t
                WHERE t.user_id = ? AND t.book_id = ? AND t.action = 'borrow'
                AND NOT EXISTS (
                    SELECT 1 FROM Transactions t2
                    WHERE t2.user_id = t.user_id AND t2.book_id = t.book_id AND t2.action = 'return'
                    AND t2.timestamp > t.timestamp
                )
                """,
                (user_id, book_id)
            )
            if not self.cursor.fetchone():
                return False, f"User ID {user_id} has not borrowed '{book[1]}'"
                
            # Update available copies and record transaction
            self.cursor.execute(
                "UPDATE Books SET available_copies = available_copies + 1 WHERE book_id = ?",
                (book_id,)
            )
            self.cursor.execute(
                """
                INSERT INTO Transactions (user_id, book_id, action, timestamp)
                VALUES (?, ?, 'return', ?)
                """,
                (user_id, book_id, datetime.now().isoformat())
            )
            self.conn.commit()
            return True, ""
        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"

    def get_books(self) -> List[Dict[str, Any]]:
        """
        Retrieve all books in the library.
        
        Returns:
            List[Dict[str, Any]]: List of book dictionaries.
        """
        self.cursor.execute("SELECT * FROM Books")
        return [dict(row) for row in self.cursor.fetchall()]

    def get_users(self) -> List[Dict[str, Any]]:
        """
        Retrieve all registered users.
        
        Returns:
            List[Dict[str, Any]]: List of user dictionaries.
        """
        self.cursor.execute("SELECT * FROM Users")
        return [dict(row) for row in self.cursor.fetchall()]

    def get_transactions(self) -> List[Dict[str, Any]]:
        """
        Retrieve all transactions.
        
        Returns:
            List[Dict[str, Any]]: List of transaction dictionaries.
        """
        self.cursor.execute("SELECT * FROM Transactions")
        return [dict(row) for row in self.cursor.fetchall()]