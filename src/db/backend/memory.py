type StudentRecord = tuple[int, str, str, int, str]

class Database:
    def __init__(self) -> None:
        self._students: list[StudentRecord] = []
        self._next_id = 1

    def create_record(
        self,
        first_name: str,
        second_name: str,
        age: int,
        gender: str,
    ) -> StudentRecord:
        if age < 0:
            raise ValueError("Возраст не может быть отрицательным.")

        student_id = self._next_id
        self._next_id += 1

        new_record: StudentRecord = (
            student_id,
            first_name.strip(),
            second_name.strip(),
            age,
            gender.strip(),
        )

        self._students.append(new_record)
        return new_record

    def get_all(self) -> list[StudentRecord]:
        return self._students.copy()

    def select_record(
        self,
        student_id: int | None = None,
        first_name: str | None = None,
        second_name: str | None = None,
        age: int | None = None,
        gender: str | None = None,
    ) -> list[StudentRecord]:
        result = self._students.copy()

        if student_id is not None:
            result = [r for r in result if r[0] == student_id]
        if first_name is not None:
            result = [r for r in result if r[1] == first_name]
        if second_name is not None:
            result = [r for r in result if r[2] == second_name]
        if age is not None:
            result = [r for r in result if r[3] == age]
        if gender is not None:
            result = [r for r in result if r[4] == gender]

        return result

    def update_record(
        self,
        student_id: int,
        first_name: str | None = None,
        second_name: str | None = None,
        age: int | None = None,
        gender: str | None = None,
    ) -> StudentRecord:
        for i, record in enumerate(self._students):
            if record[0] == student_id:
                new_record = list(record)
                if first_name is not None:
                    new_record[1] = first_name.strip()
                if second_name is not None:
                    new_record[2] = second_name.strip()
                if age is not None:
                    if age < 0:
                        raise ValueError("Возраст не может быть отрицательным.")
                    new_record[3] = age
                if gender is not None:
                    new_record[4] = gender.strip()

                updated = tuple(new_record)
                self._students[i] = updated
                return updated

        raise ValueError(f"Запись с id={student_id} не найдена.")

    def delete_record(self, student_id: int) -> StudentRecord:
        for i, record in enumerate(self._students):
            if record[0] == student_id:
                return self._students.pop(i)

        raise ValueError(f"Запись с id={student_id} не найдена.")