# memory.py

MAX_HISTORY = 6  # Only keep the last 6 turns for brevity

# In-memory store (per session)
chat_memory = []

def add_to_memory(role, content):
    chat_memory.append({"role": role, "content": content})
    # Trim to last N turns to avoid context overload
    if len(chat_memory) > MAX_HISTORY:
        del chat_memory[0]

def get_memory():
    return chat_memory
