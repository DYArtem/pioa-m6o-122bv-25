import unittest
import os
from src.db.backend.memory import Database
from src.db.backend.file_database import FileDatabase
from src.db.backend.csv_database import CSVDatabase

class TestMemory(unittest.TestCase):
    def setUp(self):
        self.db = Database()
        self.db.create_table("students", ["name", "age"])

    def test_insert(self):
        r = self.db.insert("students", ("Ivan", 20))
        self.assertEqual(r[1], "Ivan")

    def test_select(self):
        self.db.insert("students", ("Ivan", 20))
        res = self.db.select("students", {1: "Ivan"})
        self.assertEqual(len(res), 1)

    def test_update(self):
        r = self.db.insert("students", ("Ivan", 20))
        self.db.update("students", r[0], {1: "Petr"})
        self.assertEqual(self.db.select("students", {1: "Petr"})[0][1], "Petr")

    def test_delete(self):
        r = self.db.insert("students", ("Ivan", 20))
        self.db.delete("students", r[0])
        self.assertEqual(len(self.db.get_all("students")), 0)

class TestFile(unittest.TestCase):
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

class TestCSV(unittest.TestCase):
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

if __name__ == "__main__":
    unittest.main()