class BookDB:
    def __init__(self):
        self.books = []
        self.next_id = 1

    def add(self, title, author, year, status):
        book = {
            "id": self.next_id,
            "title": title,
            "author": author,
            "year": year,
            "status": status
        }
        self.books.append(book)
        self.next_id += 1
        return book

    def get_all(self):
        return self.books

    def filter(self, field, value):
        result = []
        for book in self.books:
            if str(book.get(field, "")).lower() == str(value).lower():
                result.append(book)
        return result

    def update(self, book_id, title=None, author=None, year=None, status=None):
        for book in self.books:
            if book["id"] == book_id:
                if title:
                    book["title"] = title
                if author:
                    book["author"] = author
                if year:
                    book["year"] = year
                if status:
                    book["status"] = status
                return book
        return None

    def delete(self, book_id):
        for i, book in enumerate(self.books):
            if book["id"] == book_id:
                del self.books[i]
                return True
        return False

    def sort(self, field, reverse=False):
        return sorted(self.books, key=lambda x: x.get(field, ""), reverse=reverse)