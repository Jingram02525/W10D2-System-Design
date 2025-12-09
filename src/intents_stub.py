"""
Independent intents engine with in-memory tasks list.
Run: python -m src.intents_stub
"""

_tasks = []  # in-memory list so this module runs without storage

def detect_intent(user_input: str) -> tuple[str, dict]:
    s = (user_input or "").strip().lower()
    if s in ("help", "h", "?"):
        return "HELP", {}
    for kw in ("add ", "create "):
        if s.startswith(kw):
            return "CREATE", {"task": user_input[len(kw):].strip()}
    if s in ("list", "show", "ls"):
        return "LIST", {}
    for kw in ("remove ", "delete "):
        if s.startswith(kw):
            return "DELETE", {"task": user_input[len(kw):].strip()}
    return "UNKNOWN", {}

def handle_intent(intent: str, slots: dict) -> str:
    if intent == "HELP":
        return "Try: 'add buy milk', 'list', 'remove buy milk', or 'quit'."
    if intent == "CREATE":
        name = (slots.get("task") or "").strip()
        if not name:
            return "Please include a task name. Example: add buy milk"
        _tasks.append(name)
        return f"Added: {name}"
    if intent == "LIST":
        if not _tasks:
            return "No tasks yet."
        lines = [f"Your tasks ({len(_tasks)}):"]
        for i, t in enumerate(_tasks, 1):
            lines.append(f"  {i}. {t}")
        return "\n".join(lines)
    if intent == "DELETE":
        name = (slots.get("task") or "").strip()
        if not name:
            return "Please include a task to remove. Example: remove buy milk"
        try:
            _tasks.remove(name)
            return f"Removed: {name}"
        except ValueError:
            return f"Task not found: {name}"
    return "I did not understand. Type 'help'."

def _demo_loop():
    print("Intents Stub (in-memory) — type 'help' or 'quit'")
    while True:
        text = input("> ")
        if text.strip().lower() in ("quit", "exit"):
            print("Goodbye.")
            break
        intent, slots = detect_intent(text)
        print(handle_intent(intent, slots))

if __name__ == "__main__":
    _demo_loop()
