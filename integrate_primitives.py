"""
Prometheus Integration Layer
Connects the four core primitives (Reward, State Reducer, Rollback, Context Tracer)
into the existing LangGraph agent workflow.
"""

from reward_evaluator import MultiObjectiveReward, TraceEvaluation
from state_reducer import StateReducer, UnifiedMemoryState, PatchOperation
from rollback_protocol import RollbackSaga, ResourceAllocation, ResourceType
from context_tracer import BidirectionalContextTracer, PRDConstraint, CodeNodeTrace

import ast
from typing import Dict, List, Optional
from uuid import uuid4

# ============================================
# INTEGRATION: Multi-Objective Reward (Vector 1)
# ============================================

reward_evaluator = MultiObjectiveReward(
    alpha=0.55, beta=0.25, gamma=0.15, lambda_=0.05
)

def evaluate_generated_code(
    code: str,
    test_results: Dict[str, bool],
    token_count: int,
    requirements: List[str]
) -> Dict:
    """
    Use this in your Reviewer or Executor step.
    Replaces simple 'tests_passed' with multi-objective scoring.
    """
    trace = TraceEvaluation(
        trace_id=str(uuid4()),
        requirements=requirements,
        generated_code=code,
        token_count=token_count,
        test_results=test_results
    )
    
    final_reward = reward_evaluator.evaluate(trace)
    breakdown = reward_evaluator.get_breakdown(trace)
    
    return {
        "final_reward": final_reward,
        "breakdown": breakdown,
        "should_accept": final_reward > 0.65   # Tunable threshold
    }


# ============================================
# INTEGRATION: State Reducer (Vector 2)
# ============================================

state_reducer = StateReducer()
shared_memory = UnifiedMemoryState()

def create_agent_patch(agent_id: str, target: str, operation: str, content: str = None):
    """Helper for agents to create patches safely"""
    return state_reducer.create_patch(
        agent_id=agent_id,
        target_node_id=target,
        operation=operation,
        content=content,
        current_state=shared_memory
    )

def merge_agent_patches(patches: List[PatchOperation]):
    """Call this after multiple agents produce patches"""
    global shared_memory
    shared_memory = state_reducer.merge(shared_memory, patches)
    return shared_memory


# ============================================
# INTEGRATION: Rollback Protocol (Vector 3)
# ============================================

def create_infrastructure_saga() -> RollbackSaga:
    """Create a new saga when starting infrastructure work"""
    return RollbackSaga(saga_id=str(uuid4()))


# ============================================
# INTEGRATION: Context Tracer (Vector 4)
# ============================================

context_tracer = BidirectionalContextTracer()

def register_prd_requirements(requirements: List[Dict]):
    """Call this at the beginning of a run with parsed PRD"""
    for req in requirements:
        constraint = PRDConstraint(
            constraint_id=req.get("id", str(uuid4())),
            section=req.get("section", "unknown"),
            text=req.get("text", ""),
            priority=req.get("priority", 1)
        )
        context_tracer.register_prd_constraint(constraint)

def trace_code_against_prd(code: str, prd_constraint_ids: List[str], file_path: str = "output.py"):
    """Call this after code is generated to create bidirectional links"""
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                context_tracer.trace_code_node(
                    node=node,
                    file_path=file_path,
                    prd_constraint_ids=prd_constraint_ids
                )
    except Exception as e:
        print(f"[ContextTracer] Failed to trace code: {e}")

def get_traceability_report():
    """Get full PRD ↔ Code mapping"""
    return context_tracer.export_trace_graph()


# ============================================
# Usage Example (for your main.py)
# ============================================

def example_integration_flow():
    """
    Example of how to use these in your Planner → Coder → Reviewer flow.
    """
    # 1. At start of run
    register_prd_requirements([
        {"id": "req_001", "section": "Core Logic", "text": "Function must add two numbers"}
    ])
    
    # 2. After code is generated
    generated_code = "def add(a, b): return a + b"
    evaluation = evaluate_generated_code(
        code=generated_code,
        test_results={"test_add": True},
        token_count=42,
        requirements=["Must add two numbers"]
    )
    
    print("Reward Evaluation:", evaluation)
    
    # 3. Trace the code
    trace_code_against_prd(generated_code, ["req_001"])
    
    return evaluation
