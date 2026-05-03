from .base import BaseAgent
from prometheus_core.memory.skill_manager import save_skill
from prometheus_core.memory.git_rollback import commit_skill

class ReflectionAgent(BaseAgent):
    def __init__(self):
        super().__init__("Reflection")

    def run(self, task: str):
        self.log(f"Reflecting on: {task}")
        skill_content = f"## Reflection\n{task}\n\n## Learning\nThis was successful."
        skill_name = f"reflection_{hash(task) % 10000}"
        
        try:
            save_skill(skill_name, skill_content)
            commit_skill(skill_name)
        except Exception as e:
            print(f"[Reflection] Error saving skill: {e}")
        
        return f"Reflection on: {task}"
