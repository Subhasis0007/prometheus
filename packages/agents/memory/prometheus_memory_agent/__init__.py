import json
import os

MEMORY_FILE = "episodic_memory.json"

def save_mission(goal: str, final_code: str):
    """Saves a successful mission to the local memory store."""
    memory = []
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            memory = json.load(f)
    
    memory.append({
        "goal": goal,
        "pattern": final_code[:500] # We store a snippet to guide future logic
    })
    
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)
    
    return "[MEMORY] Mission pattern indexed."

def recall_relevant_patterns(goal: str):
    """Retrieves patterns that might help with the current goal."""
    if not os.path.exists(MEMORY_FILE):
        return ""
        
    with open(MEMORY_FILE, "r") as f:
        memory = json.load(f)
    
    # For now, we do a simple keyword match (v1 architecture)
    keywords = goal.lower().split()
    relevant = [m["pattern"] for m in memory if any(k in m["goal"].lower() for k in keywords)]
    
    if relevant:
        return "\n\nRelevant past patterns to reuse:\n" + "\n---\n".join(relevant[:2])
    return ""
