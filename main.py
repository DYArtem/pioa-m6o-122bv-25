from database import BookDB

db = BookDB()

db.add("Я", "Знаю", 1112, "в наличии")
db.add("Лень", "2х Лень", 1111, "выдана")

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
        books = db.get_all()
        if not books:
            print("Нет книг")
        else:
            for b in books:
                print(f"{b['id']} | {b['title']} | {b['author']} | {b['year']} | {b['status']}")
    
    elif choice == "2":
        title = input("Название: ")
        author = input("Автор: ")
        try:
            year = int(input("Год: "))
        except:
            print("Год должен быть числом")
            continue
        status = input("Статус (в наличии/выдана): ")
        db.add(title, author, year, status)
        print("Книга добавлена")
    
    elif choice == "3":
        field = input("Искать по полю (title/author/year/status): ")
        value = input("Что искать: ")
        results = db.filter(field, value)
        if not results:
            print("Ничего не найдено")
        else:
            for b in results:
                print(f"{b['id']} | {b['title']} | {b['author']} | {b['year']} | {b['status']}")
    
    elif choice == "4":
        try:
            book_id = int(input("ID книги: "))
            print("Оставьте поле пустым, если не хотите менять")
            title = input("Новое название: ")
            author = input("Новый автор: ")
            year = input("Новый год: ")
            status = input("Новый статус: ")
            
            year = int(year) if year else None
            
            result = db.update(book_id, title, author, year, status)
            if result:
                print("Книга обновлена")
            else:
                print("Книга не найдена")
        except:
            print("Ошибка ввода")
    
    elif choice == "5":
        try:
            book_id = int(input("ID книги: "))
            if db.delete(book_id):
                print("Книга удалена")
            else:
                print("Книга не найдена")
        except:
            print("Ошибка!!")
    
    elif choice == "6":
        field = input("Сортировать по полю (title/author/year/status): ")
        order = input("1 - по возрастанию, 2 - по убыванию: ")
        reverse = (order == "2")
        sorted_books = db.sort(field, reverse)
        for b in sorted_books:
            print(f"{b['id']} | {b['title']} | {b['author']} | {b['year']} | {b['status']}")
    
    elif choice == "7":
        print("ПОКА")
        break
    
    else:
        print("НЕПРАВИЛЬНО. Введите 1-7")