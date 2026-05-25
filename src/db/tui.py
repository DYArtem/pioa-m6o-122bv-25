from .backend.memory import Database


class TUI:

    def __init__(self) -> None:
        self.db = Database()
        self._current_table: str | None = None
        self._table_fields: dict[str, list[str]] = {}
        self._init_sample_data()

    def _init_sample_data(self) -> None:
        try:
            self.db.create_table("students")
            self._table_fields["students"] = ["first_name", "second_name", "age", "gender"]
            self.db.create_record(
                "students",
                tuple(self._table_fields["students"]),
                ("Иван", "Петров", 20, "М"),
            )
            self.db.create_record(
                "students",
                tuple(self._table_fields["students"]),
                ("Мария", "Иванова", 19, "Ж"),
            )
            self._current_table = "students"
        except ValueError:
            pass

    def _print_menu(self) -> None:
        print(f"\n=== Текущая таблица: {self._current_table or 'не выбрана'} ===")
        print("1. Создать таблицу")
        print("2. Выбрать таблицу")
        print("3. Добавить запись")
        print("4. Показать все записи")
        print("5. Найти записи")
        print("6. Обновить запись")
        print("7. Удалить запись")
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

    def _print_records(self, records: list[tuple], fields: list[str]) -> None:
        if not records:
            print("Записи не найдены.")
            return

        header = "id | " + " | ".join(fields)
        print("\n" + header)
        print("-" * len(header))
        for record in records:
            print(" | ".join(str(x) for x in record))

    def _create_table(self) -> None:
        print("\nСоздание новой таблицы")
        name = input("Имя таблицы: ").strip()
        if not name:
            print("Ошибка: имя не может быть пустым.")
            return

        fields_input = input("Поля (через запятую, без id): ").strip()
        if not fields_input:
            print("Ошибка: нужно указать хотя бы одно поле.")
            return

        fields = [f.strip() for f in fields_input.split(",")]
        try:
            self.db.create_table(name)
            self._table_fields[name] = fields
            print(f"Таблица '{name}' создана. Поля: id, {', '.join(fields)}")
        except ValueError as e:
            print(f"Ошибка: {e}")

    def _select_table(self) -> None:
        tables = self.db.get_table_names()
        if not tables:
            print("Нет таблиц. Сначала создайте таблицу (пункт 1).")
            return

        print("Доступные таблицы:", ", ".join(tables))
        name = input("Имя таблицы: ").strip()
        if name in tables:
            self._current_table = name
            print(f"Переключились на таблицу '{name}'")
        else:
            print(f"Таблица '{name}' не найдена.")

    def _add_record(self) -> None:
        if not self._current_table:
            print("Сначала выберите таблицу (пункт 2).")
            return

        fields = self._table_fields.get(self._current_table, [])
        if not fields:
            print("Ошибка: поля таблицы не определены.")
            return

        print("\nДобавление записи")
        values = []
        for f in fields:
            val = input(f"{f}: ").strip()
            if f == "age":
                try:
                    val = int(val)
                except ValueError:
                    print("Ошибка: возраст должен быть числом.")
                    return
            values.append(val)

        try:
            record = self.db.create_record(
                self._current_table, tuple(fields), tuple(values)
            )
            print(f"Запись добавлена: {record}")
        except ValueError as e:
            print(f"Ошибка: {e}")

    def _show_all(self) -> None:
        if not self._current_table:
            print("Сначала выберите таблицу (пункт 2).")
            return

        try:
            records = self.db.get_all(self._current_table)
            fields = self._table_fields.get(self._current_table, [])
            self._print_records(records, fields)
        except ValueError as e:
            print(f"Ошибка: {e}")

    def _find_records(self) -> None:
        if not self._current_table:
            print("Сначала выберите таблицу (пункт 2).")
            return

        fields = self._table_fields.get(self._current_table, [])
        print("\nПоиск по фильтру (Enter = пропустить поле)")
        filters = {}
        for i, f in enumerate(fields, start=1):
            val = input(f"{f}: ").strip()
            if val:
                if f == "age":
                    try:
                        val = int(val)
                    except ValueError:
                        print("Ошибка: возраст должен быть числом.")
                        return
                filters[i] = val

        try:
            records = self.db.select_record(self._current_table, filters or None)
            self._print_records(records, fields)
        except ValueError as e:
            print(f"Ошибка: {e}")

    def _update_record(self) -> None:
        if not self._current_table:
            print("Сначала выберите таблицу (пункт 2).")
            return

        fields = self._table_fields.get(self._current_table, [])
        record_id = self._read_int("ID записи для обновления: ")

        print("Оставьте поле пустым, если не хотите менять")
        updates = {}
        for i, f in enumerate(fields, start=1):
            val = input(f"{f}: ").strip()
            if val:
                if f == "age":
                    try:
                        val = int(val)
                    except ValueError:
                        print("Ошибка: возраст должен быть числом.")
                        return
                updates[i] = val

        if not updates:
            print("Ничего не изменено.")
            return

        try:
            record = self.db.update_record(self._current_table, record_id, updates)
            print(f"Запись обновлена: {record}")
        except ValueError as e:
            print(f"Ошибка: {e}")

    def _delete_record(self) -> None:
        if not self._current_table:
            print("Сначала выберите таблицу (пункт 2).")
            return

        record_id = self._read_int("ID записи для удаления: ")

        try:
            record = self.db.delete_record(self._current_table, record_id)
            print(f"Запись удалена: {record}")
        except ValueError as e:
            print(f"Ошибка: {e}")

    def run(self) -> None:
        while True:
            self._print_menu()
            action = input("Выберите действие: ").strip()

            if action == "1":
                self._create_table()
            elif action == "2":
                self._select_table()
            elif action == "3":
                self._add_record()
            elif action == "4":
                self._show_all()
            elif action == "5":
                self._find_records()
            elif action == "6":
                self._update_record()
            elif action == "7":
                self._delete_record()
            elif action == "0":
                print("Выход из программы.")
                break
            else:
                print("Неизвестная команда. Повторите ввод.")
