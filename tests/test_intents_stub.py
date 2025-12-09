import unittest

from src.intents_stub import detect_intent, handle_intent


class TestIntentsStub(unittest.TestCase):
    def test_create_and_list_and_delete(self):
        # add
        intent, slots = detect_intent("add buy milk")
        self.assertEqual(intent, "CREATE")
        self.assertIn("Added", handle_intent(intent, slots))

        # list
        intent, slots = detect_intent("list")
        out = handle_intent(intent, slots)
        self.assertIn("Your tasks (", out)
        self.assertIn("buy milk", out)

        # remove
        intent, slots = detect_intent("remove buy milk")
        self.assertEqual(intent, "DELETE")
        self.assertIn("Removed", handle_intent(intent, slots))

    def test_unknown(self):
        intent, slots = detect_intent("asdf qwer")
        self.assertEqual(intent, "UNKNOWN")
        self.assertIn("did not understand", handle_intent(intent, slots).lower())

if __name__ == "__main__":
    unittest.main()
