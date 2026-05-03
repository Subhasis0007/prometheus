class FailureLearner:
    def learn_from_failure(self, task: str, error: str):
        """Learn from failure and give useful suggestion"""
        if "syntax" in error.lower():
            return "💡 Suggestion: Fix syntax error before execution"
        elif "timeout" in error.lower():
            return "💡 Suggestion: Increase timeout or optimize code"
        elif "permission" in error.lower():
            return "💡 Suggestion: Check file permissions"
        else:
            return "💡 Suggestion: Review the task and try a different approach"
