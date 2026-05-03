from prometheus_core.correction.mistake_detector import MistakeDetector

mistake_detector = MistakeDetector()

def check_and_suggest_rollback(task: str) -> dict:
    """Check if rollback should be suggested"""
    if mistake_detector.suggest_rollback(task):
        return {
            "should_rollback": True,
            "message": f"⚠️ This task has failed {len(mistake_detector.failure_history.get(task, []))} times. Consider rolling back to a previous version.",
            "action": "Run: prometheus rollback last"
        }
    return {"should_rollback": False}
