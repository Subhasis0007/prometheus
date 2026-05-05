"""
Enhanced Reviewer with Multi-Objective Reward Evaluation
Replaces simple binary "tests passed" logic with the full reward function.
"""

from reward_evaluator import MultiObjectiveReward, TraceEvaluation
from typing import Dict, List, Tuple
from uuid import uuid4

reward_evaluator = MultiObjectiveReward(
    alpha=0.55,      # Requirement Accuracy weight
    beta=0.25,       # Token Cost weight
    gamma=0.15,      # Code Elegance weight
    lambda_=0.05     # Complexity penalty
)

def enhanced_review(
    generated_code: str,
    test_results: Dict[str, bool],
    token_count: int,
    requirements: List[str],
    min_reward_threshold: float = 0.65
) -> Tuple[bool, Dict]:
    """
    Enhanced review step for your Coder → Reviewer flow.
    
    Returns:
        (should_accept: bool, evaluation_report: dict)
    """
    
    trace = TraceEvaluation(
        trace_id=str(uuid4()),
        requirements=requirements,
        generated_code=generated_code,
        token_count=token_count,
        test_results=test_results
    )
    
    final_reward = reward_evaluator.evaluate(trace)
    breakdown = reward_evaluator.get_breakdown(trace)
    
    should_accept = final_reward >= min_reward_threshold
    
    report = {
        "trace_id": trace.trace_id,
        "final_reward": round(final_reward, 4),
        "breakdown": breakdown,
        "should_accept": should_accept,
        "threshold": min_reward_threshold,
        "test_pass_rate": breakdown.get("accuracy", 0),
        "decision_reason": "Accepted" if should_accept else "Rejected (low multi-objective score)"
    }
    
    return should_accept, report


# Example usage inside your Reviewer node
def reviewer_node(state: dict) -> dict:
    """
    Drop-in replacement for your current reviewer logic.
    Use this pattern in your LangGraph reviewer node.
    """
    code = state.get("generated_code", "")
    tests = state.get("test_results", {})
    tokens = state.get("token_count", 0)
    requirements = state.get("requirements", [])
    
    should_accept, report = enhanced_review(
        generated_code=code,
        test_results=tests,
        token_count=tokens,
        requirements=requirements,
        min_reward_threshold=0.62   # You can tune this
    )
    
    state["review_report"] = report
    state["review_passed"] = should_accept
    
    if should_accept:
        state["status"] = "accepted"
    else:
        state["status"] = "needs_revision"
        state["feedback"] = f"Multi-objective score too low: {report['final_reward']}"
    
    return state
