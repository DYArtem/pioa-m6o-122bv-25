import unittest
import os
from src.db.backend.memory import Database
from src.db.backend.file_database import FileDatabase
from src.db.backend.csv_database import CSVDatabase


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database()

    def test_create_table(self):
        self.db.create_table("test")
        self.assertIn("test", self.db.get_table_names())

    def test_create_record(self):
        self.db.create_table("students")
        record = self.db.create_record("students", ("name", "age"), ("Ivan", 20))
        self.assertEqual(record[1], "Ivan")
        self.assertEqual(record[2], 20)

    def test_get_all(self):
        self.db.create_table("students")
        self.db.create_record("students", ("name",), ("Anna",))
        self.db.create_record("students", ("name",), ("Petr",))
        self.assertEqual(len(self.db.get_all("students")), 2)

    def test_select_by_id(self):
        self.db.create_table("students")
        self.db.create_record("students", ("name",), ("Anna",))
        r2 = self.db.create_record("students", ("name",), ("Petr",))
        result = self.db.select_record("students", {0: r2[0]})
        self.assertEqual(result[0][1], "Petr")

    def test_update_record(self):
        self.db.create_table("students")
        r = self.db.create_record("students", ("name",), ("Anna",))
        self.db.update_record("students", r[0], {1: "Anna Petrovna"})
        updated = self.db.select_record("students", {0: r[0]})
        self.assertEqual(updated[0][1], "Anna Petrovna")

    def test_delete_record(self):
        self.db.create_table("students")
        r = self.db.create_record("students", ("name",), ("Anna",))
        self.db.delete_record("students", r[0])
        self.assertEqual(len(self.db.get_all("students")), 0)

    def test_delete_not_found(self):
        self.db.create_table("students")
        with self.assertRaises(ValueError):
            self.db.delete_record("students", 999)


class TestFileDatabase(unittest.TestCase):
    def setUp(self):
        self.filename = "test_data.json"
        self.db = FileDatabase(self.filename)

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_create_table(self):
        self.db.create_table("test")
        self.assertIn("test", self.db.get_table_names())
        self.assertTrue(os.path.exists(self.filename))

    def test_create_record(self):
        self.db.create_table("students")
        record = self.db.create_record("students", ("name", "age"), ("Ivan", 20))
        self.assertEqual(record[1], "Ivan")
        self.assertEqual(record[2], 20)

    def test_save_and_load(self):
        self.db.create_table("test")
        self.db.create_record("test", ("name",), ("Anna",))
        self.db = FileDatabase(self.filename)
        self.assertIn("test", self.db.get_table_names())
        records = self.db.get_all("test")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0][1], "Anna")

    def test_get_all(self):
        self.db.create_table("students")
        self.db.create_record("students", ("name",), ("Anna",))
        self.db.create_record("students", ("name",), ("Petr",))
        self.assertEqual(len(self.db.get_all("students")), 2)

    def test_update_record(self):
        self.db.create_table("students")
        r = self.db.create_record("students", ("name",), ("Anna",))
        self.db.update_record("students", r[0], {1: "Anna Petrovna"})
        updated = self.db.select_record("students", {0: r[0]})
        self.assertEqual(updated[0][1], "Anna Petrovna")

    def test_delete_record(self):
        self.db.create_table("students")
        r = self.db.create_record("students", ("name",), ("Anna",))
        self.db.delete_record("students", r[0])
        self.assertEqual(len(self.db.get_all("students")), 0)


class TestCSVDatabase(unittest.TestCase):
    def setUp(self):
        self.filename = "test_data.csv"
        self.db = CSVDatabase(self.filename)

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_create_table(self):
        self.db.create_table("test")
        self.assertIn("test", self.db.get_table_names())
        self.assertTrue(os.path.exists(self.filename))

    def test_create_record(self):
        self.db.create_table("students")
        record = self.db.create_record("students", ("name", "age"), ("Ivan", 20))
        self.assertEqual(record[1], "Ivan")
        self.assertEqual(record[2], 20)

    def test_save_and_load(self):
        self.db.create_table("test")
        self.db.create_record("test", ("name",), ("Anna",))
        self.db = CSVDatabase(self.filename)
        self.assertIn("test", self.db.get_table_names())
        records = self.db.get_all("test")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0][1], "Anna")

    def test_get_all(self):
        self.db.create_table("students")
        self.db.create_record("students", ("name",), ("Anna",))
        self.db.create_record("students", ("name",), ("Petr",))
        self.assertEqual(len(self.db.get_all("students")), 2)

    def test_update_record(self):
        self.db.create_table("students")
        r = self.db.create_record("students", ("name",), ("Anna",))
        self.db.update_record("students", r[0], {1: "Anna Petrovna"})
        updated = self.db.select_record("students", {0: r[0]})
        self.assertEqual(updated[0][1], "Anna Petrovna")

    def test_delete_record(self):
        self.db.create_table("students")
        r = self.db.create_record("students", ("name",), ("Anna",))
        self.db.delete_record("students", r[0])
        self.assertEqual(len(self.db.get_all("students")), 0)


class TestIndexes(unittest.TestCase):
    def setUp(self):
        self.filename = "test_index.json"
        self.db = FileDatabase(self.filename)
        self.db.create_table("students")

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_create_index(self):
        self.db.create_record("students", ("name", "age"), ("Anna", 20))
        self.db.create_record("students", ("name", "age"), ("Bob", 25))
        self.db.create_index("students", "name", 1)
        result = self.db.select_record("students", {1: "Anna"})
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "Anna")

    def test_index_after_update(self):
        self.db.create_record("students", ("name", "age"), ("Anna", 20))
        self.db.create_index("students", "name", 1)
        record = self.db.select_record("students", {1: "Anna"})[0]
        self.db.update_record("students", record[0], {1: "Anna Updated"})
        result = self.db.select_record("students", {1: "Anna Updated"})
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "Anna Updated")

    def test_index_after_delete(self):
        self.db.create_record("students", ("name", "age"), ("Anna", 20))
        self.db.create_index("students", "name", 1)
        record = self.db.select_record("students", {1: "Anna"})[0]
        self.db.delete_record("students", record[0])
        result = self.db.select_record("students", {1: "Anna"})
        self.assertEqual(len(result), 0)


if __name__ == "__main__":
    unittest.main()