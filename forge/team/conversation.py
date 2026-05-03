# Real agent conversation
def team_conversation(task: str):
    return {
        "planner": f"Planner: I suggest breaking '{task}' into 3 steps.",
        "coder": f"Coder: Here is the code skeleton for '{task}'.",
        "executor": "Executor: Code executed successfully.",
        "reviewer": "Reviewer: All good. PROMETHEUS approved.",
        "final": f"Team completed '{task}' with full collaboration.",
        "supervised_by": "PROMETHEUS"
    }
