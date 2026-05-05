"""
Enhanced Bidirectional Context Tracer (Vector 4)
Maintains traceability between PRD requirements and generated code nodes.
"""

from context_tracer import BidirectionalContextTracer, PRDConstraint, CodeNodeTrace
import ast
from typing import List, Dict, Optional
from uuid import uuid4

tracer = BidirectionalContextTracer()

def load_prd_requirements(requirements: List[Dict]) -> int:
    """
    Load PRD requirements at the start of a run.
    Example:
        requirements = [
            {"id": "req_001", "section": "Core", "text": "Must support addition", "priority": 1}
        ]
    """
    count = 0
    for req in requirements:
        constraint = PRDConstraint(
            constraint_id=req.get("id", str(uuid4())),
            section=req.get("section", "General"),
            text=req.get("text", ""),
            priority=req.get("priority", 1)
        )
        tracer.register_prd_constraint(constraint)
        count += 1
    return count

def trace_generated_code(
    code: str,
    linked_constraint_ids: List[str],
    file_path: str = "artifacts/output.py"
) -> List[str]:
    """
    Trace generated code against PRD constraints.
    Call this after the Coder produces code.
    Returns list of traced node IDs.
    """
    traced_nodes = []
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                trace = tracer.trace_code_node(
                    node=node,
                    file_path=file_path,
                    prd_constraint_ids=linked_constraint_ids
                )
                traced_nodes.append(trace.node_id)
    except Exception as e:
        print(f"[Tracer] Failed to parse code: {e}")
    return traced_nodes

def get_prd_context_for_code(node_id: str) -> List[Dict]:
    """Get which PRD requirements influenced a specific code node"""
    constraints = tracer.get_prd_context_for_node(node_id)
    return [
        {"id": c.constraint_id, "section": c.section, "text": c.text}
        for c in constraints
    ]

def get_code_for_prd_requirement(constraint_id: str) -> List[Dict]:
    """Get all code nodes influenced by a specific PRD requirement"""
    nodes = tracer.get_code_nodes_for_constraint(constraint_id)
    return [
        {
            "node_id": n.node_id,
            "qualified_name": n.qualified_name,
            "file_path": n.file_path,
            "type": n.node_type
        }
        for n in nodes
    ]

def get_full_traceability_report() -> Dict:
    """Get complete PRD ↔ Code mapping for the current run"""
    return tracer.export_trace_graph()

def reset_tracer():
    """Reset tracer state between runs"""
    global tracer
    tracer = BidirectionalContextTracer()
