from .backend.memory import Database

class TUI:

    def __init__(self) -> None:
        self.db = Database()
        self._init_sample_data()

    def _init_sample_data(self) -> None:
        """Добавляет тестовые данные."""
        try:
            self.db.create_record("Иван", "Петров", 20, "М")
            self.db.create_record("Мария", "Иванова", 19, "Ж")
        except ValueError:
            pass

    def _print_menu(self) -> None:
        print("\n=== База студентов ===")
        print("1. Добавить запись")
        print("2. Показать все записи")
        print("3. Найти записи по фильтру")
        print("4. Обновить запись")
        print("5. Удалить запись")
        print("0. Выход")

    def _read_int(self, prompt: str) -> int:
        while True:
            raw = input(prompt).strip()
            try:
                return int(raw)
            except ValueError:
                print("Ошибка: введите целое число.")

    def _read_optional_int(self, prompt: str) -> int | None:
        while True:
            raw = input(prompt).strip()
            if raw == "":
                return None
            try:
                return int(raw)
            except ValueError:
                print("Ошибка: введите целое число или оставьте поле пустым.")

    def _print_records(self, records: list[tuple]) -> None:
        if not records:
            print("Записи не найдены.")
            return

        print("\nid | first_name | second_name | age | gender")
        print("-" * 60)
        for record in records:
            print(f"{record[0]} | {record[1]} | {record[2]} | {record[3]} | {record[4]}")

    def _add_student(self) -> None:
        print("\nДобавление записи")

        first_name = input("first_name: ").strip()
        second_name = input("second_name: ").strip()
        age = self._read_int("age: ")
        gender = input("gender (М/Ж): ").strip()

        try:
            record = self.db.create_record(first_name, second_name, age, gender)
            print(f"Запись добавлена: {record}")
        except ValueError as exc:
            print(f"Ошибка: {exc}")

    def _show_all_students(self) -> None:
        print("\nСписок записей")
        self._print_records(self.db.get_all())

    def _find_students_by_filter(self) -> None:
        print("\nПоиск по фильтру (Enter = пропустить поле)")

        student_id = self._read_optional_int("id: ")
        first_name = input("first_name: ").strip() or None
        second_name = input("second_name: ").strip() or None
        age = self._read_optional_int("age: ")
        gender = input("gender: ").strip() or None

        records = self.db.select_record(
            student_id=student_id,
            first_name=first_name,
            second_name=second_name,
            age=age,
            gender=gender,
        )

        self._print_records(records)

    def _update_student(self) -> None:
        print("\nОбновление записи")

        student_id = self._read_int("id записи для обновления: ")

        print("Оставьте поле пустым, если не хотите менять")
        first_name = input("first_name: ").strip() or None
        second_name = input("second_name: ").strip() or None
        age = self._read_optional_int("age: ")
        gender = input("gender: ").strip() or None

        try:
            record = self.db.update_record(student_id, first_name, second_name, age, gender)
            print(f"Запись обновлена: {record}")
        except ValueError as exc:
            print(f"Ошибка: {exc}")

    def _delete_student(self) -> None:
        print("\nУдаление записи")

        student_id = self._read_int("id записи для удаления: ")

        try:
            record = self.db.delete_record(student_id)
            print(f"Запись удалена: {record}")
        except ValueError as exc:
            print(f"Ошибка: {exc}")

    def run(self) -> None:
	while True:
            self._print_menu()
            action = input("Выберите действие: ").strip()

            if action == "1":
                self._add_student()
            elif action == "2":
                self._show_all_students()
            elif action == "3":
                self._find_students_by_filter()
            elif action == "4":
                self._update_student()
            elif action == "5":
                self._delete_student()
            elif action == "0":
                print("Выход из программы.")
                break
            else:
                print("Неизвестная команда. Повторите ввод.")