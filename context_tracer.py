from pydantic import BaseModel
from typing import List, Dict, Optional
from uuid import uuid4
import ast
import hashlib

class PRDConstraint(BaseModel):
    """A single requirement or constraint from the PRD"""
    constraint_id: str
    section: str
    text: str
    priority: int = 1

class CodeNodeTrace(BaseModel):
    """Bidirectional link between a code node and its originating PRD constraints"""
    node_id: str                    # Stable identifier (e.g. function name + hash)
    node_type: str                  # FunctionDef, ClassDef, etc.
    file_path: str
    qualified_name: str
    prd_constraint_ids: List[str]
    trace_id: str
    metadata: Dict = {}

class BidirectionalContextTracer:
    """
    Maintains bidirectional traceability between PRD and generated code.
    Every AST node knows which PRD constraint(s) created it.
    """

    def __init__(self):
        self.prd_constraints: Dict[str, PRDConstraint] = {}
        self.code_traces: Dict[str, CodeNodeTrace] = {}      # node_id → trace
        self.reverse_index: Dict[str, List[str]] = {}        # constraint_id → list of node_ids

    def register_prd_constraint(self, constraint: PRDConstraint):
        self.prd_constraints[constraint.constraint_id] = constraint

    def trace_code_node(self, node: ast.AST, file_path: str, 
                        prd_constraint_ids: List[str]) -> CodeNodeTrace:
        """
        Create a bidirectional trace for an AST node.
        Call this during code generation.
        """
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            qualified_name = node.name
            node_type = type(node).__name__
        else:
            qualified_name = getattr(node, 'name', 'unknown')
            node_type = type(node).__name__

        # Create stable node ID
        node_id = self._generate_stable_node_id(file_path, qualified_name)

        trace = CodeNodeTrace(
            node_id=node_id,
            node_type=node_type,
            file_path=file_path,
            qualified_name=qualified_name,
            prd_constraint_ids=prd_constraint_ids,
            trace_id=str(uuid4()),
            metadata={
                "lineno": getattr(node, 'lineno', None),
                "col_offset": getattr(node, 'col_offset', None)
            }
        )

        # Store forward mapping
        self.code_traces[node_id] = trace

        # Build reverse index (constraint → nodes)
        for cid in prd_constraint_ids:
            if cid not in self.reverse_index:
                self.reverse_index[cid] = []
            if node_id not in self.reverse_index[cid]:
                self.reverse_index[cid].append(node_id)

        return trace

    def get_prd_context_for_node(self, node_id: str) -> List[PRDConstraint]:
        """Given a code node, return all PRD constraints that influenced it"""
        if node_id not in self.code_traces:
            return []
        constraint_ids = self.code_traces[node_id].prd_constraint_ids
        return [self.prd_constraints[cid] for cid in constraint_ids if cid in self.prd_constraints]

    def get_code_nodes_for_constraint(self, constraint_id: str) -> List[CodeNodeTrace]:
        """Given a PRD constraint, return all code nodes it influenced"""
        node_ids = self.reverse_index.get(constraint_id, [])
        return [self.code_traces[nid] for nid in node_ids if nid in self.code_traces]

    def _generate_stable_node_id(self, file_path: str, qualified_name: str) -> str:
        """Create a stable hash-based ID for the node"""
        raw = f"{file_path}:{qualified_name}"
        return hashlib.md5(raw.encode()).hexdigest()[:12]

    def export_trace_graph(self) -> Dict:
        """Export the full bidirectional traceability graph"""
        return {
            "total_prd_constraints": len(self.prd_constraints),
            "total_code_nodes": len(self.code_traces),
            "traces": [
                {
                    "node_id": t.node_id,
                    "qualified_name": t.qualified_name,
                    "file_path": t.file_path,
                    "linked_prd_constraints": t.prd_constraint_ids
                }
                for t in self.code_traces.values()
            ]
        }
