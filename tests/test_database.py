import unittest
import os
from src.db.backend.memory import Database
from src.db.backend.file_database import FileDatabase
from src.db.backend.csv_database import CSVDatabase


class TestMemory(unittest.TestCase):
    def setUp(self):
        self.db = Database()

    def test_create_table_ok(self):
        self.db.create_table("students", ["name", "age"])
        self.assertIn("students", self.db.get_table_names())

    def test_create_table_already_exists(self):
        self.db.create_table("students", ["name", "age"])
        with self.assertRaises(ValueError):
            self.db.create_table("students", ["name", "age"])

    def test_insert_ok(self):
        self.db.create_table("students", ["name", "age"])
        r = self.db.insert("students", ("Ivan", 20))
        self.assertEqual(r[1], "Ivan")

    def test_insert_wrong_field_count(self):
        self.db.create_table("students", ["name", "age"])
        with self.assertRaises(ValueError):
            self.db.insert("students", ("Ivan",))

    def test_select_by_field(self):
        self.db.create_table("students", ["name", "age"])
        self.db.insert("students", ("Ivan", 20))
        self.db.insert("students", ("Maria", 19))
        res = self.db.select("students", {"name": "Ivan"})
        self.assertEqual(len(res), 1)

    def test_select_unknown_field(self):
        self.db.create_table("students", ["name", "age"])
        with self.assertRaises(ValueError):
            self.db.select("students", {"xxx": "Ivan"})

    def test_update_ok(self):
        self.db.create_table("students", ["name", "age"])
        r = self.db.insert("students", ("Ivan", 20))
        self.db.update("students", r[0], {"name": "Petr"})
        self.assertEqual(self.db.select("students", {"name": "Petr"})[0][1], "Petr")

    def test_update_unknown_field(self):
        self.db.create_table("students", ["name", "age"])
        r = self.db.insert("students", ("Ivan", 20))
        with self.assertRaises(ValueError):
            self.db.update("students", r[0], {"xxx": "Petr"})

    def test_delete_ok(self):
        self.db.create_table("students", ["name", "age"])
        r = self.db.insert("students", ("Ivan", 20))
        self.db.delete("students", r[0])
        self.assertEqual(len(self.db.get_all("students")), 0)

    def test_delete_not_found(self):
        self.db.create_table("students", ["name", "age"])
        with self.assertRaises(ValueError):
            self.db.delete("students", 999)


class TestFileDatabase(unittest.TestCase):
    def setUp(self):
        self.filename = "test.json"
        self.db = FileDatabase(self.filename)
        self.db.create_table("students", ["name", "age"])

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_save_load(self):
        self.db.insert("students", ("Test", 99))
        self.db = FileDatabase(self.filename)
        self.assertEqual(len(self.db.get_all("students")), 1)

    def test_corrupted_file(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            f.write("not json")
        with self.assertRaises(ValueError):
            FileDatabase(self.filename)

    def test_select_by_field(self):
        self.db.insert("students", ("Anna", 25))
        res = self.db.select("students", {"name": "Anna"})
        self.assertEqual(len(res), 1)

    def test_update_ok(self):
        r = self.db.insert("students", ("Old", 30))
        self.db.update("students", r[0], {"name": "New"})
        self.assertEqual(self.db.select("students", {"name": "New"})[0][1], "New")

    def test_delete_ok(self):
        r = self.db.insert("students", ("ToDelete", 40))
        self.db.delete("students", r[0])
        self.assertEqual(len(self.db.get_all("students")), 0)


class TestCSVDatabase(unittest.TestCase):
    def setUp(self):
        self.filename = "test.csv"
        self.db = CSVDatabase(self.filename)
        self.db.create_table("students", ["name", "age"])

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_save_load(self):
        self.db.insert("students", ("Test", 99))
        self.db = CSVDatabase(self.filename)
        self.assertEqual(len(self.db.get_all("students")), 1)

    def test_select_by_field(self):
        self.db.insert("students", ("Anna", 25))
        res = self.db.select("students", {"name": "Anna"})
        self.assertEqual(len(res), 1)

    def test_update_ok(self):
        r = self.db.insert("students", ("Old", 30))
        self.db.update("students", r[0], {"name": "New"})
        self.assertEqual(self.db.select("students", {"name": "New"})[0][1], "New")

    def test_delete_ok(self):
        r = self.db.insert("students", ("ToDelete", 40))
        self.db.delete("students", r[0])
        self.assertEqual(len(self.db.get_all("students")), 0)


if __name__ == "__main__":
    unittest.main()