# Contributing

This started as a self-directed portfolio project (simulated client engagement — see the README), but it's genuinely open to feedback, testing, and contributions.

## Ways to help

- **Try it and report what breaks.** Clone it, run it against the sample docs, and open an issue if something doesn't work as described.
- **Suggest improvements.** Retrieval tuning, prompt wording, test coverage, architecture — all fair game.
- **Open a PR.** Small, focused changes are easiest to review. If it's a bigger change, open an issue first to discuss the approach before writing code.

## Setup for local testing

1. `python3 -m venv venv && source venv/bin/activate`
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and add your own Groq API key
4. `python3 ingest.py` (builds the local vector store)
5. `uvicorn app:app --reload`
6. Visit `http://127.0.0.1:8000/`

## Reporting an issue

Include:
- What you did (the question you asked, or the command you ran)
- What you expected vs. what actually happened
- Any error output/traceback

## Code style

Nothing enforced strictly yet — keep it readable, keep functions single-purpose, and add a docstring if the function's job isn't obvious from its name.
