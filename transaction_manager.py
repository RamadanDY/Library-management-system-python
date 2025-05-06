from datetime import datetime

class TransactionManager:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

    def borrow_book(self, user_id, book_id):
        self.cursor.execute("SELECT user_id FROM Users WHERE user_id = ?", (user_id,))
        if not self.cursor.fetchone():
            print(f"User ID {user_id} not found.")
            return False
        self.cursor.execute("SELECT book_id, available_copies, title FROM Books WHERE book_id = ?", (book_id,))
        book = self.cursor.fetchone()
        if not book:
            print(f"Book ID {book_id} not found.")
            return False
        if book[1] <= 0:
            print(f"No copies of '{book[2]}' available.")
            return False
        self.cursor.execute('''
            SELECT t.book_id FROM Transactions t
            WHERE t.user_id = ? AND t.book_id = ? AND t.action = 'borrow'
            AND NOT EXISTS (
                SELECT 1 FROM Transactions t2
                WHERE t2.user_id = t.user_id AND t2.book_id = t.book_id AND t2.action = 'return'
                AND t2.timestamp > t.timestamp
            )
        ''', (user_id, book_id))
        if self.cursor.fetchone():
            print(f"User already borrowed '{book[2]}'.")
            return False
        self.cursor.execute('''
            UPDATE Books SET available_copies = available_copies - 1 WHERE book_id = ?
        ''', (book_id,))
        self.cursor.execute('''
            INSERT INTO Transactions (user_id, book_id, action, timestamp)
            VALUES (?, ?, 'borrow', ?)
        ''', (user_id, book_id, datetime.now().isoformat()))
        self.conn.commit()
        print(f"Book '{book[2]}' borrowed by user ID {user_id}.")
        return True

    def return_book(self, user_id, book_id):
        self.cursor.execute("SELECT user_id FROM Users WHERE user_id = ?", (user_id,))
        if not self.cursor.fetchone():
            print(f"User ID {user_id} not found.")
            return False
        self.cursor.execute("SELECT book_id, title FROM Books WHERE book_id = ?", (book_id,))
        book = self.cursor.fetchone()
        if not book:
            print(f"Book ID {book_id} not found.")
            return False
        self.cursor.execute('''
            SELECT t.book_id FROM Transactions t
            WHERE t.user_id = ? AND t.book_id = ? AND t.action = 'borrow'
            AND NOT EXISTS (
                SELECT 1 FROM Transactions t2
                WHERE t2.user_id = t.user_id AND t2.book_id = t.book_id AND t2.action = 'return'
                AND t2.timestamp > t.timestamp
            )
        ''', (user_id, book_id))
        if not self.cursor.fetchone():
            print(f"User ID {user_id} has not borrowed '{book[1]}'.")
            return False
        self.cursor.execute('''
            UPDATE Books SET available_copies = available_copies + 1 WHERE book_id = ?
        ''', (book_id,))
        self.cursor.execute('''
            INSERT INTO Transactions (user_id, book_id, action, timestamp)
            VALUES (?, ?, 'return', ?)
        ''', (user_id, book_id, datetime.now().isoformat()))
        self.conn.commit()
        print(f"Book '{book[1]}' returned by user ID {user_id}.")
        return True

    def display_transactions(self):
        self.cursor.execute("SELECT * FROM Transactions")
        transactions = self.cursor.fetchall()
        if not transactions:
            print("No transactions recorded.")
            return
        print("\nTransaction History:")
        for t in transactions:
            print(f"Transaction ID: {t[0]}, User ID: {t[1]}, Book ID: {t[2]}, Action: {t[3]}, Time: {t[4]}")