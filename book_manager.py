class BookManager:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

    def add_book(self, book_id, title, author, total_copies):
        self.cursor.execute("SELECT book_id FROM Books WHERE book_id = ?", (book_id,))
        if self.cursor.fetchone():
            print(f"Book ID {book_id} already exists.")
            return False
        self.cursor.execute('''
            INSERT INTO Books (book_id, title, author, total_copies, available_copies)
            VALUES (?, ?, ?, ?, ?)
        ''', (book_id, title, author, total_copies, total_copies))
        self.conn.commit()
        print(f"Book '{title}' added successfully.")
        return True

    def display_books(self):
        self.cursor.execute("SELECT * FROM Books")
        books = self.cursor.fetchall()
        if not books:
            print("No books in the library.")
            return
        print("\nLibrary Books:")
        for book in books:
            print(f"Book ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Available: {book[4]}/{book[3]}")