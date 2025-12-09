import unittest

from src.formatter import format_task_list


class TestFormatter(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(format_task_list([]), "No tasks.")

    def test_list(self):
        out = format_task_list(["a", "b"])
        self.assertIn("Your tasks (2):", out)
        self.assertIn("1. a", out)
        self.assertIn("2. b", out)

if __name__ == "__main__":
    unittest.main()
