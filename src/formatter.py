"""
Independent formatter for task lists.
Run: python -m src.formatter
"""

def format_task_list(tasks: list[str]) -> str:
    if not tasks:
        return "No tasks."
    lines = [f"Your tasks ({len(tasks)}):"]
    for i, t in enumerate(tasks, 1):
        lines.append(f"  {i}. {t}")
    return "\n".join(lines)

def _demo():
    print(format_task_list(["buy milk", "finish homework"]))

if __name__ == "__main__":
    _demo()
