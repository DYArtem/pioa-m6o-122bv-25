import unittest
from src.db.tui import TUI

class TestTUI(unittest.TestCase):
    def test_tui_creates(self):
        try:
            tui = TUI()
            self.assertIsNotNone(tui)
        except Exception as e:
            self.fail(f"TUI не создаётся: {e}")

    def test_tui_has_run(self):
        tui = TUI()
        self.assertTrue(hasattr(tui, 'run'), "Нет метода run")

if __name__ == "__main__":
    unittest.main()

