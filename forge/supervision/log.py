import json
from datetime import datetime

def log_supervision(framework: str, task: str, result: str):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "framework": framework,
        "task": task,
        "result": result[:200],
        "supervised_by": "PROMETHEUS"
    }
    with open("forge/supervision/logs.json", "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    print(f"[PROMETHEUS] Supervised {framework}: {task}")
