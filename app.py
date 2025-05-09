from flask import Flask, jsonify, request
import storage

app = Flask(__name__)


@app.route('/api/books', methods=['GET'])
def get_books():
    # For now, we'll return a static list
    books = storage.load_json("data.json")
    return jsonify(books)

@app.route('/api/books', methods=['GET', 'POST'])
def books():
    if request.method == 'GET':
        # Handle the GET request
        # For now, we'll return a static list
        books = storage.load_json("data.json")
        return jsonify(books)

    elif request.method == 'POST':
        # Handle the POST request
        # For now, we'll just return the data the user sent
        # Later, we'll add code to save the new book in our data storage
        new_book = request.get_json()
        storage.add_book(new_book)
        return jsonify(new_book), 201


@app.route('/api/books/<int:id>', methods=['PUT'])
def handle_book(id):
    # Find the book with the given ID
    book = storage.find_book_by_id(id)

    # If the book wasn't found, return a 404 error
    if book is None:
        return '', 404

    # Update the book with the new data
    new_data = request.get_json()
    updated_book = storage.update_book(book, new_data)
    # Return the updated book
    return jsonify(updated_book)


@app.route('/api/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    # Find the book with the given ID
    book = storage.find_book_by_id(id)

    # If the book wasn't found, return a 404 error
    if book is None:
        return '', 404

    # Remove the book from the list
    deleted_book = storage.delete_book(id)

    # Return the deleted book
    return jsonify(deleted_book)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
