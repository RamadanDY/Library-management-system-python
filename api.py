from flask import Flask, request, jsonify
from flask_cors import CORS
from library import Library

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests
library = Library()

@app.route('/books', methods=['GET'])
def get_books():
    books = []
    library.cursor.execute("SELECT * FROM Books")
    for book in library.cursor.fetchall():
        books.append({
            'book_id': book[0],
            'title': book[1],
            'author': book[2],
            'total_copies': book[3],
            'available_copies': book[4]
        })
    return jsonify(books)

@app.route('/users', methods=['GET'])
def get_users():
    users = []
    library.cursor.execute("SELECT * FROM Users")
    for user in library.cursor.fetchall():
        users.append({
            'user_id': user[0],
            'name': user[1]
        })
    return jsonify(users)

@app.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = []
    library.cursor.execute("SELECT * FROM Transactions")
    for t in library.cursor.fetchall():
        transactions.append({
            'transaction_id': t[0],
            'user_id': t[1],
            'book_id': t[2],
            'action': t[3],
            'timestamp': t[4]
        })
    return jsonify(transactions)

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    success = library.add_book(
        data['book_id'],
        data['title'],
        data['author'],
        data['total_copies']
    )
    return jsonify({'success': success}), 201 if success else 400

@app.route('/users', methods=['POST'])
def register_user():
    data = request.get_json()
    success = library.register_user(
        data['user_id'],
        data['name']
    )
    return jsonify({'success': success}), 201 if success else 400

@app.route('/borrow', methods=['POST'])
def borrow_book():
    data = request.get_json()
    success = library.borrow_book(
        data['user_id'],
        data['book_id']
    )
    return jsonify({'success': success}), 200 if success else 400

@app.route('/return', methods=['POST'])
def return_book():
    data = request.get_json()
    success = library.return_book(
        data['user_id'],
        data['book_id']
    )
    return jsonify({'success': success}), 200 if success else 400

if __name__ == '__main__':
    app.run(debug=True)