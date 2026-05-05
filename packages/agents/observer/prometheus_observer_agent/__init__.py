import os

def observe_project(root_dir: str = "."):
    """
    Surgically scans ONLY the agent packages to keep context lean.
    """
    context = "Project Context (Core Agents Only):\n"
    # We only care about our custom packages, not the root bloat
    target_dir = os.path.join(root_dir, "packages")
    
    if not os.path.exists(target_dir):
        return "No local packages found."

    for root, dirs, files in os.walk(target_dir):
        # Ignore pycache
        if "__pycache__" in dirs:
            dirs.remove("__pycache__")
            
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                context += f"\n-- File: {path} --\n"
                with open(path, "r") as f:
                    # Only take the first 500 chars (Function signatures only)
                    context += f.read()[:500] + "\n... (truncated)\n"
                    
    return context
