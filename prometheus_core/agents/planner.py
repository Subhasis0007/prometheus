from .base import BaseAgent

class PlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__("Planner")

    def run(self, task: str):
        self.log(f"Planning: {task}")
        return f"Plan for: {task}"
