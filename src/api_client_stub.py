"""
OpenAI API client stub (beginner-friendly)

Usage:
  # Live call (requires OPENAI_API_KEY in env)
  python -m src.api_client_stub --prompt "Explain Pomodoro in one sentence."

  # Specify model (default: gpt-4o-mini) and optional system prompt
  python -m src.api_client_stub --model gpt-4o-mini --system "You are concise." --prompt "What is JSON?"

  # Mock (no network needed): read the answer from a local text file
  python -m src.api_client_stub --mock samples/answer.txt
"""

import argparse
import json
import os
from typing import Optional

# Optional deps
try:
    from openai import OpenAI  # modern SDK
except Exception:
    OpenAI = None  # type: ignore

try:
    import requests
except Exception:
    requests = None  # type: ignore


class LlmError(Exception):
    pass


def _clean_one_line(text: str, max_len: int = 240) -> str:
    """Make a short one-liner for CLI output."""
    s = " ".join((text or "").strip().split())
    if len(s) > max_len:
        s = s[: max_len - 1] + "…"
    return s


def ask_openai(
    prompt: str,
    model: str = "gpt-4o-mini",
    system: Optional[str] = None,
    temperature: float = 0.3,
    timeout: int = 20,
) -> str:
    """
    Call OpenAI using either the SDK (preferred) or plain HTTP via requests.
    Requires OPENAI_API_KEY to be set in the environment.
    Returns a single-line string suitable for CLI printing.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise LlmError("Missing environment variable: OPENAI_API_KEY")

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    # Path 1: SDK present
    if OpenAI is not None:
        try:
            client = OpenAI(api_key=api_key)
            resp = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=256,
            )
            content = (resp.choices[0].message.content or "").strip()
            return _clean_one_line(content)
        except Exception as e:
            raise LlmError(f"OpenAI SDK call failed: {e}")

    # Path 2: Fallback to raw HTTP if requests available
    if requests is None:
        raise LlmError("Neither OpenAI SDK nor 'requests' is available. Use --mock.")

    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 256,
        }
        r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=timeout)
        if r.status_code != 200:
            # Show a short friendly error; include code only
            raise LlmError(f"HTTP {r.status_code} from OpenAI")
        data = r.json()
        content = (data["choices"][0]["message"]["content"] or "").strip()
        return _clean_one_line(content)
    except Exception as e:
        raise LlmError(f"OpenAI HTTP call failed: {e}")


def load_mock_text(path: str) -> str:
    """Read mock answer from a local text file."""
    with open(path, "r", encoding="utf-8") as f:
        return _clean_one_line(f.read())


def _main():
    parser = argparse.ArgumentParser(description="OpenAI client stub")
    parser.add_argument("--prompt", help="What you want to ask the model")
    parser.add_argument("--system", help="Optional system instruction", default=None)
    parser.add_argument("--model", help="OpenAI model (default: gpt-4o-mini)", default="gpt-4o-mini")
    parser.add_argument("--mock", help="Path to a local .txt file for offline demo")
    args = parser.parse_args()

    # Source order: live OpenAI → mock
    if args.prompt:
        try:
            answer = ask_openai(prompt=args.prompt, model=args.model, system=args.system)
            print(answer)
            return
        except Exception as e:
            print(f"LLM unavailable: {e}")
            # Fall through to mock if provided

    if args.mock:
        try:
            print(load_mock_text(args.mock))
            return
        except Exception as e:
            print(f"Mock load failed: {e}")
            return

    print("No output. Provide --prompt for live call (requires OPENAI_API_KEY) or --mock <file>.")


if __name__ == "__main__":
    _main()
