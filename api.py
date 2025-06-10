from flask import Flask, request, jsonify, g
from flask_cors import CORS
from library_manager import Library
import sqlite3
# this is also a module that is used to import the mysql db module 
from db_setup import DatabaseSetup

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Initialize database schema
db_setup = DatabaseSetup()
DATABASE = db_setup.get_db_path()

def get_db():
    """Get a database connection for the current request."""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # Enable dictionary-like row access
    return g.db

@app.teardown_appcontext
def close_db(error):
    """Close the database connection at the end of the request."""
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/books', methods=['GET'])
def get_books():
    """Retrieve all books."""
    try:
        db = get_db()
        library = Library(db)
        books = library.get_books()
        return jsonify(books)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/users', methods=['GET'])
def get_users():
    """Retrieve all users."""
    try:
        db = get_db()
        library = Library(db)
        users = library.get_users()
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/transactions', methods=['GET'])
def get_transactions():
    """Retrieve all transactions."""
    try:
        db = get_db()
        library = Library(db)
        transactions = library.get_transactions()
        return jsonify(transactions)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/books', methods=['POST'])
def add_book():
    """Add a new book."""
    try:
        data = request.get_json()
        required_fields = ['book_id', 'title', 'author', 'total_copies']
        if not data or not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
            
        db = get_db()
        library = Library(db)
        success, error = library.add_book(
            data['book_id'],
            data['title'],
            data['author'],
            data['total_copies']
        )
        if success:
            return jsonify({"success": True}), 201
        return jsonify({"error": error}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/users', methods=['POST'])
def register_user():
    """Register a new user."""
    try:
        data = request.get_json()
        required_fields = ['user_id', 'name']
        if not data or not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
            
        db = get_db()
        library = Library(db)
        success, error = library.register_user(
            data['user_id'],
            data['name']
        )
        if success:
            return jsonify({"success": True}), 201
        return jsonify({"error": error}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/borrow', methods=['POST'])
def borrow_book():
    """Borrow a book for a user."""
    try:
        data = request.get_json()
        required_fields = ['user_id', 'book_id']
        if not data or not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
            
        db = get_db()
        library = Library(db)
        success, error = library.borrow_book(
            data['user_id'],
            data['book_id']
        )
        if success:
            return jsonify({"success": True}), 200
        return jsonify({"error": error}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/return', methods=['POST'])
def return_book():
    """Return a book borrowed by a user."""
    try:
        data = request.get_json()
        required_fields = ['user_id', 'book_id']
        if not data or not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
            
        db = get_db()
        library = Library(db)
        success, error = library.return_book(
            data['user_id'],
            data['book_id']
        )
        if success:
            return jsonify({"success": True}), 200
        return jsonify({"error": error}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)