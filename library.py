from db_setup import DatabaseSetup
from book_manager import BookManager
from user_manager import UserManager
from transaction_manager import TransactionManager

class Library:
    def __init__(self, db_name="library.db"):
        self.db = DatabaseSetup(db_name)
        self.conn = self.db.get_connection()
        self.cursor = self.db.get_cursor()
        self.book_manager = BookManager(self.conn, self.cursor)
        self.user_manager = UserManager(self.conn, self.cursor)
        self.transaction_manager = TransactionManager(self.conn, self.cursor)

    def add_book(self, book_id, title, author, total_copies):
        return self.book_manager.add_book(book_id, title, author, total_copies)

    def register_user(self, user_id, name):
        return self.user_manager.register_user(user_id, name)

    def borrow_book(self, user_id, book_id):
        return self.transaction_manager.borrow_book(user_id, book_id)

    def return_book(self, user_id, book_id):
        return self.transaction_manager.return_book(user_id, book_id)

    def display_books(self):
        self.book_manager.display_books()

    def display_users(self):
        self.user_manager.display_users()

    def display_transactions(self):
        self.transaction_manager.display_transactions()

    def __del__(self):
        self.db.close()