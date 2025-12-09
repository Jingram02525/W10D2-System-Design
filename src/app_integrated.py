# src/app_integrated.py
#!/usr/bin/env python3
"""
Integrated demo app (CLI loop) wired to intents_stub and a pluggable LLM.

Run examples:
  python -m src.app_integrated --provider mock --greet
  python -m src.app_integrated --provider openai --model gpt-4o-mini --greet
  python -m src.app_integrated --provider anthropic --model claude-3-5-sonnet-latest --greet
"""

from __future__ import annotations

import argparse
from typing import Any, Callable, Dict, List, Tuple

# Use the stub intents explicitly (your repo already has intents_stub.py)
from src.intents_stub import detect_intent, handle_intent

# --- Optional LLM providers (import whichever you actually have) ---

# OpenAI client: try both names to match your repo variants
ask_openai = None
try:
    from src.api_client_openai import \
        ask_openai  # if you created api_client_openai.py
except Exception:
    pass
if ask_openai is None:
    try:
        from src.api_client_stub import \
            ask_openai  # if your stub hosts the OpenAI call
    except Exception:
        ask_openai = None  # leave as None

# Anthropic client (optional)
ask_anthropic = None
try:
    from src.api_client_anthropic import ask_anthropic
except Exception:
    ask_anthropic = None


# ---------- LLM factory ----------

def make_llm(provider: str, model: str, system: str | None) -> Callable[[str], str]:
    """
    Return a callable: (prompt: str) -> str using the selected provider.
    If provider == 'mock', returns a safe echo function.
    """
    p = (provider or "mock").strip().lower()

    if p in ("openai", "oai"):
        if ask_openai is None:
            raise RuntimeError("OpenAI client not available in this repo.")
        def _llm(prompt: str) -> str:
            return ask_openai(prompt=prompt, model=model, system=system)
        return _llm

    if p in ("anthropic", "claude"):
        if ask_anthropic is None:
            raise RuntimeError("Anthropic client not available in this repo.")
        def _llm(prompt: str) -> str:
            return ask_anthropic(prompt=prompt, model=model, system=system)
        return _llm

    # Default: offline-safe mock
    def _mock(prompt: str) -> str:
        snippet = (prompt or "")[:160].replace("\n", " ")
        return f"[mock] {snippet}"
    return _mock


# ---------- CLI parsing ----------

def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        prog="app-integrated",
        description="Capstone CLI — integrated layers + pluggable LLM",
    )
    ap.add_argument(
        "--provider",
        default="mock",
        help="openai | anthropic | mock (default: mock)",
    )
    ap.add_argument(
        "--model",
        default="gpt-4o-mini",
        help="Model name for the provider (default: gpt-4o-mini)",
    )
    ap.add_argument(
        "--system",
        default=None,
        help="Optional system instruction for the LLM",
    )
    ap.add_argument(
        "--greet",
        action="store_true",
        help="Print a greeting and quick help",
    )
    return ap.parse_args()


# ---------- Main loop ----------

def run() -> None:
    args = parse_args()

    # Build LLM callable (works even when provider=mock)
    try:
        llm = make_llm(provider=args.provider, model=args.model, system=args.system)
    except Exception as e:
        # If provider not available, drop to mock
        print(f"(LLM provider unavailable: {e} — using mock)")
        llm = make_llm(provider="mock", model="", system=None)

    if args.greet:
        print("Integrated Chat — type 'help' for examples; 'quit' to exit.\n")

    # Minimal in-memory transcript to pass along if your intents use it
    history: List[Tuple[str, str]] = []  # [(user, bot)]

    while True:
        try:
            user = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        low = user.lower()
        if low in ("quit", "exit"):
            print("Goodbye!")
            break

        if not user:
            continue

        # Detect intent + slots via your stub
        intent, slots = detect_intent(user)

        # Try to call handle_intent with richer kwargs first.
        # If the stub doesn't accept them, fall back to minimal signature.
        try:
            response = handle_intent(intent, slots, llm=llm, history=history)
        except TypeError:
            # Your stub may only accept (intent, slots) or (intent, slots, llm)
            try:
                response = handle_intent(intent, slots, llm=llm)  # type: ignore[arg-type]
            except TypeError:
                response = handle_intent(intent, slots)

                # Optional safety: if your stub signals an AI-backed action,
                # do the call here using slots["prompt"] when present.
                if intent in {"EXPLAIN", "ENCOURAGE", "ASK_AI"}:
                    try:
                        prompt = slots.get("prompt", "Give a brief, encouraging tip.")
                        ai_text = llm(prompt)
                        response = f"{response}\n{ai_text}"
                    except Exception as e:
                        response = f"{response}\n(LLM unavailable: {e})"

        print(response)
        history.append((user, response))


if __name__ == "__main__":
    run()
