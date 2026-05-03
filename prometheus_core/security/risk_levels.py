def classify_risk(task: str) -> str:
    """Classify the risk level of a task"""
    task_lower = task.lower()
    
    critical_keywords = ["delete", "format", "shutdown", "rm -rf", "kill -9"]
    high_keywords = ["remove", "drop", "truncate", "overwrite"]
    medium_keywords = ["modify", "update", "change", "edit"]
    
    if any(kw in task_lower for kw in critical_keywords):
        return "CRITICAL"
    elif any(kw in task_lower for kw in high_keywords):
        return "HIGH"
    elif any(kw in task_lower for kw in medium_keywords):
        return "MEDIUM"
    else:
        return "LOW"

def get_risk_emoji(risk_level: str) -> str:
    """Get emoji for risk level"""
    emojis = {
        "CRITICAL": "🔴",
        "HIGH": "🟠",
        "MEDIUM": "🟡",
        "LOW": "🟢"
    }
    return emojis.get(risk_level, "⚪")
