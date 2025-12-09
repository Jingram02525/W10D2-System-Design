import os
import shutil
import tempfile
import unittest

# Important: set DATA_DIR before importing storage module functions
tmp = tempfile.mkdtemp(prefix="data_dir_")
os.environ["DATA_DIR"] = tmp

from src.storage_stub import (add_task, load_tasks, remove_task,  # noqa: E402
                              save_tasks)


class TestStorageStub(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(tmp, ignore_errors=True)

    def test_roundtrip(self):
        self.assertEqual(load_tasks(), [])
        add_task("a")
        add_task("b")
        self.assertEqual(load_tasks(), ["a", "b"])
        ok = remove_task("a")
        self.assertTrue(ok)
        self.assertEqual(load_tasks(), ["b"])
        # save and reload
        save_tasks(["x", "y"])
        self.assertEqual(load_tasks(), ["x", "y"])

if __name__ == "__main__":
    unittest.main()
