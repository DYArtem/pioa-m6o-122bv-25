import unittest
from database import BookDB

class TestBookDB(unittest.TestCase):
    def setUp(self):
        self.db = BookDB()
        self.db.add("Книга1", "Автор1", 2000, "в наличии")
        self.db.add("Книга2", "Автор2", 2001, "выдана")

    def test_add(self):
        count_before = len(self.db.get_all())
        self.db.add("Новая", "Новый", 2024, "в наличии")
        count_after = len(self.db.get_all())
        self.assertEqual(count_after, count_before + 1)

    def test_get_all(self):
        books = self.db.get_all()
        self.assertEqual(len(books), 2)

    def test_filter(self):
        results = self.db.filter("author", "Автор1")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Книга1")

    def test_update(self):
        self.db.update(1, title="Изменено")
        book = self.db.get_all()[0]
        self.assertEqual(book["title"], "Изменено")

    def test_delete(self):
        self.db.delete(1)
        self.assertEqual(len(self.db.get_all()), 1)

    def test_sort(self):
        sorted_books = self.db.sort("year", reverse=False)
        self.assertEqual(sorted_books[0]["year"], 2000)
        self.assertEqual(sorted_books[1]["year"], 2001)

if __name__ == "__main__":
    unittest.main()