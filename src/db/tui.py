from .backend.memory import create_record, select_record, update_record, delete_record

next_id = 1

def _get_next_id() -> int:
    global next_id
    all_students = select_record()
    if all_students:
        max_id = max(record[0] for record in all_students)
        next_id = max_id + 1
    return next_id

def _print_menu() -> None:
    print("\n=== База студентов ===")
    print("1. Добавить запись")
    print("2. Показать все записи")
    print("3. Найти записи по фильтру")
    print("4. Обновить запись")
    print("5. Удалить запись")
    print("0. Выход")

def _read_int(prompt: str) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("Ошибка: введите целое число.")

def _read_optional_int(prompt: str) -> int | None:
    while True:
        raw = input(prompt).strip()
        if raw == "":
            return None
        try:
            return int(raw)
        except ValueError:
            print("Ошибка: введите целое число или оставьте поле пустым.")

def _print_records(records: list[tuple]) -> None:
    if not records:
        print("Записи не найдены.")
        return

    print("\nid | first_name | second_name | age | gender")
    print("-" * 60)
    for record in records:
        print(f"{record[0]} | {record[1]} | {record[2]} | {record[3]} | {record[4]}")

def _add_student() -> None:
    print("\nДобавление записи")

    student_id = _get_next_id()
    print(f"id (автоматически): {student_id}")

    first_name = input("first_name: ").strip()
    second_name = input("second_name: ").strip()
    age = _read_int("age: ")
    gender = input("gender (М/Ж): ").strip()

    try:
        record = create_record(student_id, first_name, second_name, age, gender)
        print(f"Запись добавлена: {record}")
    except ValueError as exc:
        print(f"Ошибка: {exc}")

def _show_all_students() -> None:
    print("\nСписок записей")
    _print_records(select_record())

def _find_students_by_filter() -> None:
    print("\nПоиск по фильтру (Enter = пропустить поле)")

    student_id = _read_optional_int("id: ")
    first_name = input("first_name: ").strip() or None
    second_name = input("second_name: ").strip() or None
    age = _read_optional_int("age: ")
    gender = input("gender: ").strip() or None

    records = select_record(
        student_id=student_id,
        first_name=first_name,
        second_name=second_name,
        age=age,
        gender=gender,
    )

    _print_records(records)

def _update_student() -> None:
    print("\nОбновление записи")

    student_id = _read_int("id записи для обновления: ")

    print("Оставьте поле пустым, если не хотите менять")
    first_name = input("first_name: ").strip() or None
    second_name = input("second_name: ").strip() or None
    age = _read_optional_int("age: ")
    gender = input("gender: ").strip() or None

    try:
        record = update_record(student_id, first_name, second_name, age, gender)
        print(f"Запись обновлена: {record}")
    except ValueError as exc:
        print(f"Ошибка: {exc}")

def _delete_student() -> None:
    print("\nУдаление записи")

    student_id = _read_int("id записи для удаления: ")

    try:
        record = delete_record(student_id)
        print(f"Запись удалена: {record}")
    except ValueError as exc:
        print(f"Ошибка: {exc}")

def run() -> None:
    global next_id

    # Добавим тестовые данные
    try:
        create_record(1, "Иван", "Иванов", 20, "М")
        create_record(2, "Мария", "Иванова", 19, "Ж")
        next_id = 3
    except ValueError:
        pass

    while True:
        _print_menu()
        action = input("Выберите действие: ").strip()

        if action == "1":
            _add_student()
        elif action == "2":
            _show_all_students()
        elif action == "3":
            _find_students_by_filter()
        elif action == "4":


_update_student()
        elif action == "5":
            _delete_student()
        elif action == "0":
            print("Выход из программы.")
            break
        else:
            print("Неизвестная команда. Повторите ввод.")