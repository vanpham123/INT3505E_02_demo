from flask import Flask, request, jsonify, send_file
from flask_swagger_ui import get_swaggerui_blueprint
from models import db, Book

app = Flask(__name__)

# --- Cấu hình SQLite ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# --- Swagger UI ---
SWAGGER_URL = '/docs'
API_URL = '/static/book-api.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL,
    config={'app_name': "Book Management API"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

with app.app_context():
    db.create_all()

# --- CRUD endpoints ---
@app.route('/api/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([b.to_dict() for b in books])

@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book.to_dict())

@app.route('/api/books', methods=['POST'])
def add_book():
    data = request.get_json()
    book = Book(title=data['title'], author=data['author'], year=data.get('year'), genre=data.get('genre'))
    db.session.add(book)
    db.session.commit()
    return jsonify(book.to_dict()), 201

@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    data = request.get_json()
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.year = data.get('year', book.year)
    book.genre = data.get('genre', book.genre)
    db.session.commit()
    return jsonify(book.to_dict())

@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    db.session.delete(book)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
