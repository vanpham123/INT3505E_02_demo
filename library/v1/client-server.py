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


@app.route('/books', methods=['GET'])
def get_book():
    return jsonify(books), 200


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
    return jsonify(new_book), 201


if __name__ == '__main__':
    app.run(debug=True)
