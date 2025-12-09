# src/intents_stub.py
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

# ---- Intent detection ----

def detect_intent(user_input: str) -> Tuple[str, Dict[str, str]]:
    """
    Return (intent, slots). Minimal rules:
      - "help" -> HELP
      - "hello"/"hi" -> GREET
      - "echo ..." -> ECHO with text slot
      - "ai: ..." or "explain ..." or "ask ..." -> ASK_AI with prompt slot
      - otherwise -> UNKNOWN
    """
    s = (user_input or "").strip()
    low = s.lower()

    if low in {"help", "?", "h"}:
        return "HELP", {}

    if low.startswith(("hello", "hi")):
        return "GREET", {}

    if low.startswith("echo "):
        return "ECHO", {"text": s[5:].strip()}

    # AI-backed intent: three friendly triggers
    for trigger in ("ai:", "explain ", "ask "):
        if low.startswith(trigger):
            # keep the original user text after the trigger as the prompt
            prompt = s[len(trigger):].strip()
            return "ASK_AI", {"prompt": prompt}

    return "UNKNOWN", {}

# ---- Intent handling ----

def handle_intent(
    intent: str,
    slots: Dict[str, str],
    llm: Optional[callable] = None,
    history: Optional[List[tuple[str, str]]] = None,
) -> str:
    """
    Basic responses. If intent == ASK_AI and llm is provided, call it.
    """
    if intent == "HELP":
        return ("Try:\n"
                "  • hello\n"
                "  • echo your text here\n"
                "  • ai: Explain Pomodoro in one sentence.\n"
                "  • explain how to do a plank\n"
                "  • ask what is JSON?\n"
                "Type 'quit' to exit.")

    if intent == "GREET":
        return "Hello! Ask me anything, or type 'help' for examples."

    if intent == "ECHO":
        text = slots.get("text", "")
        return text or "(nothing to echo)"

    if intent == "ASK_AI":
        prompt = slots.get("prompt", "").strip() or "Answer briefly."
        if llm is None:
            return "(AI unavailable) Provide a provider or run with --provider mock."
        try:
            answer = llm(prompt)
            return answer
        except Exception as e:
            # Friendly failure that proves resilience
            return f"(LLM unavailable: {e}) Try again later or switch to --provider mock."

    return "I didn’t understand that. Type 'help' for examples."
