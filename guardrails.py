# guardrails.py

from config import BANNED_TERMS

def is_input_safe(user_input: str) -> bool:
    lowered = user_input.lower()
    for term in BANNED_TERMS:
        if term in lowered:
            return False
    return True

def moderate_input(user_input: str) -> str:
    if not is_input_safe(user_input):
        return "🚫 Your input contains restricted terms. Please rephrase your question."
    return None
