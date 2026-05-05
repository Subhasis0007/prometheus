"""
Enhanced State Management using CRDT-style Reducer (Vector 2)
Provides safe, conflict-free state updates for multi-agent swarms.
"""

from state_reducer import StateReducer, UnifiedMemoryState, PatchOperation
from typing import Dict, List, Optional

state_reducer = StateReducer()
shared_memory = UnifiedMemoryState()

def get_shared_memory() -> UnifiedMemoryState:
    global shared_memory
    return shared_memory

def create_patch(
    agent_id: str,
    target_node: str,
    operation: str,
    content: Optional[str] = None
) -> PatchOperation:
    """
    Agents should use this to propose changes to shared memory.
    Example: Coder proposes a new function, Executor proposes a fix.
    """
    global shared_memory
    return state_reducer.create_patch(
        agent_id=agent_id,
        target_node_id=target_node,
        operation=operation,
        content=content,
        current_state=shared_memory
    )

def apply_patches(patches: List[PatchOperation]) -> Dict:
    """
    Merge multiple agent patches safely.
    Call this after Planner/Coder/Reviewer produce patches.
    """
    global shared_memory
    shared_memory = state_reducer.merge(shared_memory, patches)
    
    return {
        "status": "merged",
        "total_nodes": len(shared_memory.node_registry),
        "version_vector": shared_memory.version_vector,
        "applied_patches": len(patches)
    }

def get_node_content(node_id: str) -> Optional[str]:
    """Get current content of a node from shared memory"""
    global shared_memory
    return shared_memory.node_registry.get(node_id)

def reset_shared_memory():
    """Reset state (useful between runs)"""
    global shared_memory
    shared_memory = UnifiedMemoryState()


# LangGraph State Integration Helper
def update_langgraph_state_with_patches(state: Dict, patches: List[PatchOperation]) -> Dict:
    """
    Use this inside your LangGraph nodes to safely update shared state.
    """
    result = apply_patches(patches)
    state["shared_memory_version"] = result["version_vector"]
    state["shared_memory_nodes"] = len(result.get("node_registry", {}))
    state["last_merge_result"] = result
    return state
