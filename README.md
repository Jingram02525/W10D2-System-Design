# Capstone Sprint 1 Demo: Parts First, Integrate Live

This repo is designed for in-class demo of Sprint 1 Integration. Each component runs independently so you can show:
1) A working CLI stub
2) A working intents engine using in-memory data
3) A working storage layer writing JSON
4) A working API client (or mock)
5) A formatter

You will then wire them together in `app_integrated.py`.

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install requests  # optional; only for api_client_stub HTTP demo
python -m unittest -v
