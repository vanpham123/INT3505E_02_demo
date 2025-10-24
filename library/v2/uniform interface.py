from flask import Flask, jsonify, request

app = Flask(__name__)

books = [
    {
        "id": 1,
        "title": "Python Programming",
        "author": "Tom",
    },
    {
        "id": 2,
        "title": "C++ Programming",
        "author": "Jerry",
    }
]


@app.route('/')
def home():
    return "Home page", 200


#in ra danh sách books
@app.route('/books', methods=['GET'])
def get_book():
    return jsonify(books), 200


#in ra thông tin của 1 book
@app.route('/books/<int:id>', methods=['GET'])
def get_book_by_id(id):
    for book in books:
        if book['id'] == id:
            return jsonify(book), 200

    return jsonify({"Book not found!"}), 404


#thêm sách vào danh sách books.
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    if not data or 'title' not in data or 'author' not in data:
        return jsonify({'error': 'missing title or author'}), 400

    new_book = {
        "id": len(books) + 1,
        "title": data["title"],
        "author": data["author"],
    }
    books.append(new_book)
    return jsonify(new_book),


#cập nhật thông tin của sách theo id.
@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    data = request.get_json()
    for book in books:
        if book['id'] == id:
            book['title'] = data["title"]
            book['author'] = data["author"]
            return jsonify(book)
    return jsonify({"Book not found!"}), 404


#xóa sách trong danh sách books.
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    for book in books:
        if book['id'] == id:
            books.remove(book)
            return jsonify({"Book deleted!"}), 200
    return jsonify({"Book not found!"}), 404


if __name__ == '__main__':
    app.run(debug=True)
