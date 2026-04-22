from database import books, add_book, get_all_books, filter_books, update_book, delete_book

def show_books(book_list):
    if not book_list:
        print("Нет книг.")
        return
    print("\n" + "-" * 70)
    for b in book_list:
        print(f"{b['id']} | {b['title']} | {b['author']} | {b['year']} | {b['status']}")
    print("-" * 70)

def main():
    add_book("я", "не знаю", 1111, "в наличии")
    add_book("что-то", "какой-то", 1212, "выдана")

    while True:
        print("\n--- Меню ---")
        print("1. Показать все книги")
        print("2. Добавить книгу")
        print("3. Найти книги")
        print("4. Обновить книгу")
        print("5. Удалить книгу")
        print("6. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            show_books(get_all_books())

        elif choice == "2":
            try:
                title = input("Название: ")
                author = input("Автор: ")
                year = int(input("Год: "))
                status = input("Статус (в наличии/выдана): ")
                add_book(title, author, year, status)
            except ValueError:
                print("Ошибка: год должен быть числом")

        elif choice == "3":
            field = input("По какому полю искать (title/author/year/status): ")
            value = input("Что искать: ")
            result = filter_books(field, value)
            show_books(result)

        elif choice == "4":
            try:
                book_id = int(input("ID книги: "))
                title = input("Новое название (Enter - не менять): ")
                author = input("Новый автор (Enter - не менять): ")
                year = input("Новый год (Enter - не менять): ")
                status = input("Новый статус (Enter - не менять): ")
                update_book(book_id, title, author, year, status)
            except ValueError:
                print("Ошибка: ID должен быть числом")

        elif choice == "5":
            try:
                book_id = int(input("ID книги: "))
                delete_book(book_id)
            except ValueError:
                print("Ошибка: ID должен быть числом")

        elif choice == "6":
            print("Пока!")
            break

        else:
            print("Нет такого пункта. Введите 1-6.")

if __name__ == "__main__":
    main()