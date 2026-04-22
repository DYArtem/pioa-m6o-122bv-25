books = []
next_id = 1

def add_book(title, author, year, status):
    global next_id
    book = {
        "id": next_id,
        "title": title,
        "author": author,
        "year": year,
        "status": status
    }
    books.append(book)
    next_id += 1
    print(f"книга добавлна. ID: {book['id']}")

def get_all_books():
    return books

def filter_books(field, value):
    result = []
    for book in books:
        if str(book.get(field, "")).lower() == str(value).lower():
            result.append(book)
    return result

def update_book(book_id, title, author, year, status):
    for book in books:
        if book["id"] == book_id:
            if title:
                book["title"] = title
            if author:
                book["author"] = author
            if year:
                book["year"] = year
            if status:
                book["status"] = status
            print("Книга обновлена")
            return
    print("Ошибка: книга не найдена")

def delete_book(book_id):
    for i, book in enumerate(books):
        if book["id"] == book_id:
            del books[i]
            print("Книга удалена")
            return
    print("Ошибка: книга не найдена")