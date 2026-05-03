import json
from datetime import datetime

MEMORY_FILE = "forge/memory/persistent.json"

def save_memory(key: str, value: str):
    try:
        with open(MEMORY_FILE, "r") as f:
            memory = json.load(f)
    except:
        memory = {}
    memory[key] = {"value": value, "timestamp": datetime.now().isoformat()}
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)
    print(f"[PROMETHEUS] Saved memory: {key}")

def get_memory(key: str):
    try:
        with open(MEMORY_FILE, "r") as f:
            memory = json.load(f)
        return memory.get(key, {}).get("value", "No memory found")
    except:
        return "No memory found"
