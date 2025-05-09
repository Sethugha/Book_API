import requests

def get_some_books():
    url = "http://127.0.0.1:5000/api/books"
    counter=0
    for i in range(1,10):
        ext_url = url + f"?page={i}&limit={5}"
        response = requests.get(ext_url)
        books = response.json()
        for book in books:
            counter += 1
            print(f"Title:{book['title']}\nAuthor: {book['author']}\n")
    print(counter)


def main():
    while True:
        get_some_books()


if __name__ == '__main__':
    main()
