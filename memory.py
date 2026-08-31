# memory.py
conversation_memory: dict[str, list[dict]] = {}

def get_history(session_id: str) -> list[dict]:
    return conversation_memory.get(session_id, [])

def add_to_history(session_id: str, question: str, answer: str):
    conversation_memory.setdefault(session_id, []).append(
        {"question": question, "answer": answer}
    )