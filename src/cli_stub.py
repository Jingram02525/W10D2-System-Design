"""
Independent CLI stub.
Echoes input and shows help. No storage, no intents, no formatter.
Run: python -m src.cli_stub
"""

HELP = (
    "Commands:\n"
    "  help          Show commands\n"
    "  demo          Show a demo response\n"
    "  quit / exit   Leave the CLI\n"
)

def run_cli_stub():
    print("CLI Stub v1.0")
    print("Type 'help' for commands.\n")
    while True:
        text = input("> ").strip()
        low = text.lower()
        if low in ("quit", "exit"):
            print("Goodbye.")
            return
        if low == "help":
            print(HELP)
            continue
        if low == "demo":
            print("This is a stubbed CLI response.")
            continue
        if not text:
            continue
        print(f"(echo) {text}")

if __name__ == "__main__":
    run_cli_stub()
