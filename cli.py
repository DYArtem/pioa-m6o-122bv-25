from database import BookDB

class BookCLI:
    def __init__(self):
        self.db = BookDB()
        # Добавим тестовые книги
        self.db.add("Я", "Знаю", 1112, "в наличии")
        self.db.add("Лень", "2х Лень", 1111, "выдана")

    def run(self):
        while True:
            print("БИБЛИОТЕКА")
            print("1. Все книги")
            print("2. Добавить книгу")
            print("3. Найти книгу")
            print("4. Обновить книгу")
            print("5. Удалить книгу")
            print("6. Сортировка")
            print("7. Выход")
            
            choice = input("Выберите действие: ")
            
            if choice == "1":
                self.show_all()
            elif choice == "2":
                self.add_book()
            elif choice == "3":
                self.find_books()
            elif choice == "4":
                self.update_book()
            elif choice == "5":
                self.delete_book()
            elif choice == "6":
                self.sort_books()
            elif choice == "7":
                print("ПОКА")
                break
            else:
                print("НЕПРАВИЛЬНО. Введите 1-7")

    def show_all(self):
        books = self.db.get_all()
        if not books:
            print("Нету книг")
        else:
            for b in books:
                print(f"{b['id']} | {b['title']} | {b['author']} | {b['year']} | {b['status']}")

    def add_book(self):
        title = input("Название: ")
        author = input("Автор: ")
        try:
            year = int(input("Год: "))
        except:
            print("Год должен быть числом")
            return
        status = input("Статус (в наличии/выдана): ")
        self.db.add(title, author, year, status)
        print("Книга добавлена!")

    def find_books(self):
        field = input("Искать по полю (title/author/year/status): ")
        value = input("Что искать: ")
        results = self.db.filter(field, value)
        if not results:
            print("Ничего не найдено")
        else:
            for b in results:
                print(f"{b['id']} | {b['title']} | {b['author']} | {b['year']} | {b['status']}")

    def update_book(self):
        try:
            book_id = int(input("ID книги: "))
            print("Оставьте поле пустым если не хотите менять")
            title = input("Новое название: ")
            author = input("Новый автор: ")
            year = input("Новый год: ")
            status = input("Новый статус: ")
            
            year = int(year) if year else None
            
            result = self.db.update(book_id, title, author, year, status)
            if result:
                print("Книга обновлена")
            else:
                print("Книга не найдена")
        except:
            print("Ошибка ввода")

    def delete_book(self):
        try:
            book_id = int(input("ID книги: "))
            if self.db.delete(book_id):
                print("Книга удалена")
            else:
                print("Книга не найдена")
        except:
            print("Ошибка")

    def sort_books(self):
        field = input("Сортировать по полю (title/author/year/status): ")
        order = input("1 - по возрастанию, 2 - по убыванию: ")
        reverse = (order == "2")
        sorted_books = self.db.sort(field, reverse)
        for b in sorted_books:
            print(f"{b['id']} | {b['title']} | {b['author']} | {b['year']} | {b['status']}")