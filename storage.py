import json


def save_json(books):
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(books, file, ensure_ascii=False, indent=4)


def load_json(filepath):
    with open(filepath, 'r') as file:
        books = json.load(file)
    return books


def get_highest_id():
    ids = []
    books = load_json('data.json')
    for book in books:
        ids.append(book['id'])
    return max(ids)


def delete_book(id):
    books = load_json('data.json')
    for book in books:
        if book['id'] == id:
            books.remove(book)
            save_json(books)
            return book
    return None


def add_book(book):
    books = load_json('data.json')
    new_id = get_highest_id() + 1
    book['id'] = new_id
    books.append(book)
    save_json(books)


def find_book_by_id(id):
    books = load_json('data.json')
    for book in books:
        if book['id'] == id:
            return book
    return None


def update_book(updated_book, changes):
    books = load_json('data.json')
    for book in books:
        if book['id'] == updated_book['id']:
            book.update(changes)
            save_json(books)
            return book
    return None

def main():
    data = [
        {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
        {"id": 2, "title": "1984", "author": "George Orwell"}
    ]
    save_json(data)
    get_highest_id()

if __name__ == '__main__':
    main()
