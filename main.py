from library import Library

if __name__ == "__main__":
    library = Library()

    # Adding books
    library.add_book(1, "The Great Gatsby", "F. Scott Fitzgerald", 5)
    library.add_book(2, "1984", "George Orwell", 3)
    library.add_book(3, "2000", "Devil May Cry", 10)

    # Registering users
    library.register_user(101, "Alice Smith")
    library.register_user(102, "Bob Johnson")
    library.register_user(103, "Yakamota")

    # Display initial state
    library.display_books()
    library.display_users()

    # Borrowing books
    library.borrow_book(101, 1)
    library.borrow_book(101, 2)
    library.borrow_book(102, 1)

    # Display updated state
    library.display_books()
    library.display_users()

    # Returning books
    library.return_book(101, 1)

    # Display final state
    library.display_books()
    library.display_transactions()