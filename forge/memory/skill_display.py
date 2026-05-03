import os
def get_recent_skills(limit=5):
    skills = []
    if os.path.exists("skills"):
        files = sorted([f for f in os.listdir("skills") if f.endswith(".md")], reverse=True)[:limit]
        for filename in files:
            with open(f"skills/{filename}") as file:
                content = file.read()
                skills.append(content[:300])
    return skills
