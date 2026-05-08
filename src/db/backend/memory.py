type Record = tuple[int, ...]
type TableDict = dict[str, list[Record]]


class Database:

    def __init__(self) -> None:
        self._tables: TableDict = {}
        self._next_ids: dict[str, int] = {}

    def create_table(self, table_name: str) -> None:
        if table_name in self._tables:
            raise ValueError(f"Таблица '{table_name}' уже существует.")
        self._tables[table_name] = []
        self._next_ids[table_name] = 1

    def get_table_names(self) -> list[str]:
        return list(self._tables.keys())

    def _get_next_id(self, table_name: str) -> int:
        current = self._next_ids.get(table_name, 1)
        self._next_ids[table_name] = current + 1
        return current

    def create_record(
        self, table_name: str, fields: tuple[str, ...], values: tuple
    ) -> Record:
        if table_name not in self._tables:
            raise ValueError(f"Таблица '{table_name}' не найдена.")

        if len(fields) != len(values):
            raise ValueError("Количество полей не совпадает с количеством значений.")

        record_id = self._get_next_id(table_name)
        record = (record_id,) + values
        self._tables[table_name].append(record)
        return record

    def get_all(self, table_name: str) -> list[Record]:
        if table_name not in self._tables:
            raise ValueError(f"Таблица '{table_name}' не найдена.")
        return self._tables[table_name].copy()

    def select_record(
        self,
        table_name: str,
        filters: dict[int, object] | None = None,
    ) -> list[Record]:
        if table_name not in self._tables:
            raise ValueError(f"Таблица '{table_name}' не найдена.")

        result = self._tables[table_name].copy()

        if filters:
            for pos, value in filters.items():
                result = [r for r in result if r[pos] == value]

        return result

    def update_record(
        self,
        table_name: str,
        record_id: int,
        updates: dict[int, object],
    ) -> Record:
        if table_name not in self._tables:
            raise ValueError(f"Таблица '{table_name}' не найдена.")

        for i, record in enumerate(self._tables[table_name]):
            if record[0] == record_id:
                new_record = list(record)
                for pos, value in updates.items():
                    new_record[pos] = value
                updated = tuple(new_record)
                self._tables[table_name][i] = updated
                return updated

        raise ValueError(f"Запись с id={record_id} не найдена в '{table_name}'.")

    def delete_record(self, table_name: str, record_id: int) -> Record:
        if table_name not in self._tables:
            raise ValueError(f"Таблица '{table_name}' не найдена.")

        for i, record in enumerate(self._tables[table_name]):
            if record[0] == record_id:
                return self._tables[table_name].pop(i)

        raise ValueError(f"Запись с id={record_id} не найдена в '{table_name}'.")
