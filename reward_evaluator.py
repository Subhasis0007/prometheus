from pydantic import BaseModel
from typing import List, Dict, Optional
import ast

class TraceEvaluation(BaseModel):
    trace_id: str
    requirements: List[str]
    generated_code: str
    token_count: int
    test_results: Dict[str, bool]
    cyclomatic_complexity: Optional[int] = None

class MultiObjectiveReward:
    """
    Multi-Objective Reward Function for DSPy Optimization
    Balances: Accuracy, Cost, Elegance
    """
    def __init__(self, alpha: float = 0.55, beta: float = 0.25, 
                 gamma: float = 0.15, lambda_: float = 0.05):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.lambda_ = lambda_

    def _compute_elegance_score(self, code: str) -> float:
        try:
            tree = ast.parse(code)
            complexity = sum(
                1 for node in ast.walk(tree)
                if isinstance(node, (ast.If, ast.For, ast.While, ast.Try, ast.With))
            )
            loc = max(len(code.splitlines()), 1)
            return 1.0 / (1.0 + complexity + 0.5 * loc)
        except Exception:
            return 0.1

    def evaluate(self, trace: TraceEvaluation) -> float:
        # 1. Requirement Accuracy
        passed = sum(1 for v in trace.test_results.values() if v)
        total = max(len(trace.test_results), 1)
        accuracy = passed / total

        # 2. Token Cost (normalized, lower is better)
        cost_score = 1.0 / (1.0 + (trace.token_count ** 0.5))

        # 3. Elegance
        elegance = self._compute_elegance_score(trace.generated_code)

        # 4. Complexity Penalty
        complexity_penalty = self._compute_elegance_score(trace.generated_code) * 0.3

        # Final Scalar Reward
        reward = (
            self.alpha * accuracy +
            self.beta * cost_score +
            self.gamma * elegance -
            self.lambda_ * complexity_penalty
        )

        return max(0.0, min(1.0, reward))

    def get_breakdown(self, trace: TraceEvaluation) -> Dict[str, float]:
        """Returns individual component scores for debugging"""
        passed = sum(1 for v in trace.test_results.values() if v)
        total = max(len(trace.test_results), 1)
        accuracy = passed / total
        cost_score = 1.0 / (1.0 + (trace.token_count ** 0.5))
        elegance = self._compute_elegance_score(trace.generated_code)

        return {
            "accuracy": round(accuracy, 4),
            "cost_score": round(cost_score, 4),
            "elegance": round(elegance, 4),
            "final_reward": round(self.evaluate(trace), 4)
        }
