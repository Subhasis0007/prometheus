import os
from datetime import datetime

# Use absolute path to avoid relative path issues
SKILL_DIR = os.path.abspath("skills")
os.makedirs(SKILL_DIR, exist_ok=True)

def save_skill(name: str, content: str):
    filepath = os.path.join(SKILL_DIR, f"{name}.md")
    with open(filepath, "w") as f:
        f.write(f"# {name}\n\n")
        f.write(f"**Created:** {datetime.now().isoformat()}\n\n")
        f.write(content)
    print(f"[Skill] Saved: {name}")
