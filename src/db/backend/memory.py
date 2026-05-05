type StudentRecord = tuple[int, str, str, int, str]

Student: list[StudentRecord] = []

def create_record(
    student_id: int,
    first_name: str,
    second_name: str,
    age: int,
    gender: str,
) -> StudentRecord:
    if age < 0:
        raise ValueError("Возраст не может быть отрицательным.")

    if any(record[0] == student_id for record in Student):
        raise ValueError(f"Запись с id={student_id} уже существует.")

    new_record: StudentRecord = (
        student_id,
        first_name.strip(),
        second_name.strip(),
        age,
        gender.strip(),
    )

    Student.append(new_record)
    return new_record

def select_record(
    student_id: int | None = None,
    first_name: str | None = None,
    second_name: str | None = None,
    age: int | None = None,
    gender: str | None = None,
) -> list[StudentRecord]:
    if (
        student_id is None
        and first_name is None
        and second_name is None
        and age is None
        and gender is None
    ):
        return Student.copy()

    result: list[StudentRecord] = []

    for record in Student:
        if student_id is not None and record[0] != student_id:
            continue
        if first_name is not None and record[1] != first_name:
            continue
        if second_name is not None and record[2] != second_name:
            continue
        if age is not None and record[3] != age:
            continue
        if gender is not None and record[4] != gender:
            continue
        result.append(record)

    return result

def update_record(
    student_id: int,
    first_name: str | None = None,
    second_name: str | None = None,
    age: int | None = None,
    gender: str | None = None,
) -> StudentRecord:
    for i, record in enumerate(Student):
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
            Student[i] = updated
            return updated

    raise ValueError(f"Запись с id={student_id} не найдена.")

def delete_record(student_id: int) -> StudentRecord:
    for i, record in enumerate(Student):
        if record[0] == student_id:
            return Student.pop(i)

    raise ValueError(f"Запись с id={student_id} не найдена.")