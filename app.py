import logging
from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import storage

app = Flask(__name__)
limiter = Limiter(app=app, key_func=get_remote_address)

#configure logging
logging.basicConfig(filename='log.txt', filemode='w', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
@app.route('/api/books', methods=['GET'])
@limiter.limit("10/minute") #Limit to 10 requests per minute
def handle_books():
    #app.logger.info('GET request received for /api/books')
    books = storage.load_json("data.json")
    author = request.args.get('author')
    title = request.args.get('title')
    if author:
        collection = [book for book in books if book.get('author') == author]
        return jsonify(collection)

    if title:
        collection = [book for book in books if book.get('title') == title]
        return jsonify(collection)

    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    if page and limit:
        start_index = (page - 1) * limit
        end_index = start_index + limit
        paginated_books = books[start_index:end_index]
        return jsonify(paginated_books)

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
        if not validate_book_data(new_book):
            return jsonify({"error": "Invalid book data"}), 400
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


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Book Not Found or Wrong Url"}), 404


@app.errorhandler(405)
def method_not_allowed_error(error):
    return jsonify({"error": "Method Not Allowed"}), 405


@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Request is in bad shape. Missing some field data?"}), 400


def validate_book_data(data):
    if "title" not in data or "author" not in data:
        return False
    return True




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
