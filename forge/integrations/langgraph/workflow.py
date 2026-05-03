from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    next: str

def langgraph_supervisor(state: AgentState):
    """PROMETHEUS supervises LangGraph workflows"""
    print("[Forge] PROMETHEUS supervising LangGraph workflow")
    return {"next": "end"}

graph = StateGraph(AgentState)
graph.add_node("supervisor", langgraph_supervisor)
graph.set_entry_point("supervisor")
graph.add_edge("supervisor", END)

langgraph_workflow = graph.compile()
