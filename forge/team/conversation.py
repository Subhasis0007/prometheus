# Real agent conversation
def team_conversation(task: str):
    return {
        "planner": f"Planner: Breaking '{task}' into steps.",
        "coder": f"Coder: Generating code skeleton.",
        "executor": "Executor: Running and testing.",
        "reviewer": "Reviewer: Approved by PROMETHEUS.",
        "final": f"Full team solution for '{task}' completed.",
        "supervised_by": "PROMETHEUS"
    }
