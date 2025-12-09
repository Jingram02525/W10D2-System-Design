"""
Independent API client for tiny JSON GET, with mock loader.
Requires 'requests' for live HTTP, but mock works without it.
Run:
  python -m src.api_client_stub --todo-id 1
  python -m src.api_client_stub --mock samples/todo1.json
"""

import argparse
import json
from typing import Any, Dict, Optional

try:
    import requests  # optional
except Exception:
    requests = None

class HttpError(Exception):
    pass

def fetch_todo(todo_id: int, timeout: int = 5) -> Dict[str, Any]:
    if requests is None:
        raise HttpError("HTTP disabled. Install requests or use --mock.")
    url = f"https://jsonplaceholder.typicode.com/todos/{todo_id}"
    try:
        r = requests.get(url, timeout=timeout)
        if r.status_code != 200:
            raise HttpError(f"HTTP {r.status_code}")
        return r.json()
    except Exception as e:
        raise HttpError(f"Network error: {e}")

def load_mock(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def summarize_todo(todo: Dict[str, Any]) -> str:
    tid = todo.get("id", "?")
    title = (todo.get("title") or "").strip() or "Untitled"
    done = bool(todo.get("completed", False))
    status = "[DONE]" if done else "[TODO]"
    return f"{status} #{tid}: {title}"

def _main():
    parser = argparse.ArgumentParser(description="API client stub demo")
    parser.add_argument("--todo-id", type=int, help="Fetch sample TODO by id")
    parser.add_argument("--mock", help="Path to local mock JSON")
    args = parser.parse_args()

    data: Optional[Dict[str, Any]] = None
    if args.todo_id is not None:
        try:
            data = fetch_todo(args.todo_id)
        except Exception as e:
            print(f"HTTP unavailable: {e}")

    if data is None:
        if not args.mock:
            print("No data available. Provide --todo-id or --mock.")
            return
        data = load_mock(args.mock)

    print(summarize_todo(data))

if __name__ == "__main__":
    _main()
