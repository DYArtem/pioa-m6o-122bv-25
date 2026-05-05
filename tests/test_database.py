import unittest
from src.db.backend.memory import Database

class TestDatabase(unittest.TestCase):

    def setUp(self) -> None:
        self.db = Database()

    def test_create_record(self) -> None:
        record = self.db.create_record("Анна", "Сидорова", 21, "Ж")
        self.assertEqual(record[1], "Анна")
        self.assertEqual(record[2], "Сидорова")
        self.assertEqual(record[3], 21)
        self.assertEqual(record[4], "Ж")

    def test_get_all(self) -> None:
        self.db.create_record("Анна", "Сидорова", 21, "Ж")
        self.db.create_record("Петр", "Иванов", 22, "М")
        all_records = self.db.get_all()
        self.assertEqual(len(all_records), 2)

    def test_select_by_id(self) -> None:
        self.db.create_record("Анна", "Сидорова", 21, "Ж")
        record2 = self.db.create_record("Петр", "Иванов", 22, "М")
        result = self.db.select_record(student_id=record2[0])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "Петр")

    def test_select_by_first_name(self) -> None:
        self.db.create_record("Анна", "Сидорова", 21, "Ж")
        self.db.create_record("Петр", "Иванов", 22, "М")
        result = self.db.select_record(first_name="Анна")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][2], "Сидорова")

    def test_update_record(self) -> None:
        record = self.db.create_record("Анна", "Сидорова", 21, "Ж")
        self.db.update_record(record[0], first_name="Анна Петровна")
        updated = self.db.select_record(student_id=record[0])
        self.assertEqual(updated[0][1], "Анна Петровна")

    def test_delete_record(self) -> None:
        record = self.db.create_record("Анна", "Сидорова", 21, "Ж")
        self.db.delete_record(record[0])
        all_records = self.db.get_all()
        self.assertEqual(len(all_records), 0)

    def test_delete_not_found(self) -> None:
        with self.assertRaises(ValueError):
            self.db.delete_record(999)

if __name__ == "__main__":
    unittest.main()