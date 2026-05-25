import unittest
from src.db.backend.memory import Database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database()

    def test_create_table(self):
        self.db.create_table("test")
        self.assertIn("test", self.db.get_table_names())

    def test_create_record(self):
        self.db.create_table("students")
        record = self.db.create_record("students", ("name", "age"), ("Иван", 20))
        self.assertEqual(record[1], "Иван")
        self.assertEqual(record[2], 20)

    def test_get_all(self):
        self.db.create_table("students")
        self.db.create_record("students", ("name",), ("Анна",))
        self.db.create_record("students", ("name",), ("Петр",))
        self.assertEqual(len(self.db.get_all("students")), 2)

    def test_select_by_id(self):
        self.db.create_table("students")
        self.db.create_record("students", ("name",), ("Анна",))
        r2 = self.db.create_record("students", ("name",), ("Петр",))
        result = self.db.select_record("students", {0: r2[0]})
        self.assertEqual(result[0][1], "Петр")

    def test_update_record(self):
        self.db.create_table("students")
        r = self.db.create_record("students", ("name",), ("Анна",))
        self.db.update_record("students", r[0], {1: "Анна Петровна"})
        updated = self.db.select_record("students", {0: r[0]})
        self.assertEqual(updated[0][1], "Анна Петровна")

    def test_delete_record(self):
        self.db.create_table("students")
        r = self.db.create_record("students", ("name",), ("Анна",))
        self.db.delete_record("students", r[0])
        self.assertEqual(len(self.db.get_all("students")), 0)

    def test_delete_not_found(self):
        self.db.create_table("students")
        with self.assertRaises(ValueError):
            self.db.delete_record("students", 999)

if __name__ == "__main__":
    unittest.main()
