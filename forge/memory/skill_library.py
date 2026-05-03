import os
import re
import logging
from typing import List, Dict

logger = logging.getLogger("PROMETHEUS-Skills")

class SkillLibrary:
    def __init__(self, skills_dir: str = "forge/skills"):
        self.skills_dir = skills_dir
        os.makedirs(self.skills_dir, exist_ok=True)

    def crystallize_skill(self, task_description: str, transcript: List[Dict[str, str]]):
        """Extracts the final approved code and saves it as a reusable skill."""
        logger.info("Attempting to crystallize skill from approved transcript...")
        
        final_code = None
        # Walk backwards through the transcript to find the last thing the Coder wrote
        for entry in reversed(transcript):
            if entry["agent"] == "Coder":
                content = entry["content"]
                # Extract code block
                if "```python" in content:
                    final_code = content.split("```python")[1].split("```")[0].strip()
                elif "```" in content:
                    final_code = content.split("```")[1].split("```")[0].strip()
                break
                
        if not final_code:
            logger.warning("Could not extract python code to save as a skill.")
            return

        # Create a safe filename from the task description
        filename = re.sub(r'[^a-z0-9]', '_', task_description.lower()[:30].strip('_')) + ".md"
        filepath = os.path.join(self.skills_dir, filename)

        # Format the skill document
        skill_doc = f"# Task: {task_description}\n\n"
        skill_doc += "## Verified Implementation\n"
        skill_doc += f"```python\n{final_code}\n```\n"

        with open(filepath, 'w') as f:
            f.write(skill_doc)
            
        logger.info(f"✅ Skill successfully crystallized: {filename}")

    def get_available_skills(self) -> str:
        """Returns a string summary of known skills for the Researcher."""
        skills = []
        for filename in os.listdir(self.skills_dir):
            if filename.endswith(".md"):
                filepath = os.path.join(self.skills_dir, filename)
                with open(filepath, 'r') as f:
                    # Read just the first line (the task description)
                    first_line = f.readline().strip().replace("# Task: ", "")
                    skills.append(f"- {first_line}")
        
        if not skills:
            return "No prior skills crystallized yet."
        return "Known Skills in Memory:\n" + "\n".join(skills)
