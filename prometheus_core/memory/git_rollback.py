import subprocess
import os

SKILL_DIR = "skills"
os.makedirs(SKILL_DIR, exist_ok=True)

def commit_skill(skill_name: str):
    os.chdir(SKILL_DIR)
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", f"Added skill: {skill_name}"])
    print(f"[Git] Committed skill: {skill_name}")
