class MistakeDetector:
    def __init__(self):
        self.failure_history = {}
    
    def record_failure(self, task: str, error: str):
        if task not in self.failure_history:
            self.failure_history[task] = []
        self.failure_history[task].append(error)
    
    def detect_repeated_failure(self, task: str) -> bool:
        if task in self.failure_history:
            return len(self.failure_history[task]) >= 3
        return False
