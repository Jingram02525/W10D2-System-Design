"""
Independent JSON storage to a data folder.
Respects DATA_DIR env var. Defaults to ./data
Run examples:
  python -m src.storage_stub --add "buy milk"
  python -m src.storage_stub --list
  python -m src.storage_stub --remove "buy milk"
"""

import argparse
import json
import os


def _data_dir() -> str:
    return os.environ.get("DATA_DIR", "data")

def _data_file() -> str:
    return os.path.join(_data_dir(), "tasks.json")

def _ensure_dir():
    os.makedirs(_data_dir(), exist_ok=True)

def load_tasks() -> list[str]:
    _ensure_dir()
    path = _data_file()
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [str(x) for x in data] if isinstance(data, list) else []
    except Exception:
        return []

def save_tasks(tasks: list[str]) -> None:
    _ensure_dir()
    with open(_data_file(), "w", encoding="utf-8") as f:
        json.dump(list(tasks), f, indent=2)

def add_task(name: str) -> None:
    tasks = load_tasks()
    tasks.append(name)
    save_tasks(tasks)

def remove_task(name: str) -> bool:
    tasks = load_tasks()
    if name in tasks:
        tasks.remove(name)
        save_tasks(tasks)
        return True
    return False

def _main():
    parser = argparse.ArgumentParser(description="Storage stub demo")
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--add", help="Add a task")
    g.add_argument("--remove", help="Remove a task")
    g.add_argument("--list", action="store_true", help="List tasks")
    args = parser.parse_args()

    if args.add:
        add_task(args.add)
        print(f"Added: {args.add}")
        return
    if args.remove:
        ok = remove_task(args.remove)
        print("Removed." if ok else "Task not found.")
        return
    if args.list:
        tasks = load_tasks()
        if not tasks:
            print("No tasks.")
            return
        for i, t in enumerate(tasks, 1):
            print(f"{i}. {t}")

if __name__ == "__main__":
    _main()
