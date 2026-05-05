from pydantic import BaseModel
from typing import Dict, List, Optional
from uuid import uuid4
import time

class PatchOperation(BaseModel):
    """Represents a single atomic change to shared memory"""
    op_id: str
    agent_id: str
    timestamp: float
    target_node_id: str          # Stable identifier for AST node / memory key
    operation: str               # "insert", "replace", "delete"
    content: Optional[str] = None
    version_vector: Dict[str, int]

class UnifiedMemoryState(BaseModel):
    """Shared state across all agents in the swarm"""
    version_vector: Dict[str, int] = {}
    patches: List[PatchOperation] = []
    node_registry: Dict[str, str] = {}   # node_id -> current content

class StateReducer:
    """
    CRDT-style deterministic merge for multi-agent state.
    Prevents O(N²) synchronization and conflicting AST patches.
    """

    def create_patch(self, agent_id: str, target_node_id: str, 
                     operation: str, content: Optional[str] = None,
                     current_state: Optional[UnifiedMemoryState] = None) -> PatchOperation:
        """Create a new patch with proper version vector"""
        vv = current_state.version_vector.copy() if current_state else {}
        vv[agent_id] = vv.get(agent_id, 0) + 1

        return PatchOperation(
            op_id=str(uuid4()),
            agent_id=agent_id,
            timestamp=time.time(),
            target_node_id=target_node_id,
            operation=operation,
            content=content,
            version_vector=vv
        )

    def merge(self, current: UnifiedMemoryState, 
              incoming_patches: List[PatchOperation]) -> UnifiedMemoryState:
        """
        Deterministic, conflict-free merge.
        Uses version vectors + causal ordering.
        """
        new_state = current.model_copy(deep=True)

        # Sort by timestamp then agent_id for deterministic ordering
        sorted_patches = sorted(
            incoming_patches, 
            key=lambda p: (p.timestamp, p.agent_id)
        )

        for patch in sorted_patches:
            node_id = patch.target_node_id

            # Check if this patch is causally ready
            is_ready = all(
                new_state.version_vector.get(aid, 0) >= patch.version_vector.get(aid, 0)
                for aid in patch.version_vector
            )

            if is_ready:
                # Apply operation
                if patch.operation in ["replace", "insert"]:
                    new_state.node_registry[node_id] = patch.content or ""
                elif patch.operation == "delete":
                    new_state.node_registry.pop(node_id, None)

                # Update version vector
                for aid, ver in patch.version_vector.items():
                    new_state.version_vector[aid] = max(
                        new_state.version_vector.get(aid, 0), ver
                    )

                new_state.patches.append(patch)

        return new_state

    def get_state_summary(self, state: UnifiedMemoryState) -> Dict:
        return {
            "total_nodes": len(state.node_registry),
            "total_patches": len(state.patches),
            "version_vector": state.version_vector
        }
