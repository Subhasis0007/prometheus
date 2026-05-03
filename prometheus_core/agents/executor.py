from .base import BaseAgent
from prometheus_core.execution.sandbox import run_in_sandbox
from prometheus_core.security.human_loop import requires_approval, request_approval
from prometheus_core.security.risk_levels import classify_risk, get_risk_emoji
from prometheus_core.security.audit import log_action
from prometheus_core.correction.mistake_detector import MistakeDetector
from prometheus_core.correction.failure_learner import FailureLearner

mistake_detector = MistakeDetector()
failure_learner = FailureLearner()

class ExecutorAgent(BaseAgent):
    def __init__(self):
        super().__init__("Executor")

    def run(self, task: str):
        risk_level = classify_risk(task)
        risk_emoji = get_risk_emoji(risk_level)
        
        self.log(f"Risk: {risk_emoji} {risk_level}")
        
        if requires_approval(task):
            if not request_approval(task):
                return "❌ Task cancelled by user"
        
        result = run_in_sandbox(task)
        
        if result["success"]:
            log_action(self.name, task, "SUCCESS", risk_level)
            return f"✅ Executed: {result['output'][:100]}..."
        else:
            mistake_detector.record_failure(task, result['error'])
            suggestion = failure_learner.learn_from_failure(task, result['error'])
            
            log_action(self.name, task, "FAILED", risk_level)
            return f"❌ Failed: {result['error']}\n{suggestion}"
