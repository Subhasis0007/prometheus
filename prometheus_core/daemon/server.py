from fastapi import FastAPI, Query
import uvicorn
from prometheus_core.agents.planner import PlannerAgent
from prometheus_core.agents.coder import CoderAgent
from prometheus_core.agents.executor import ExecutorAgent
from prometheus_core.agents.reflection import ReflectionAgent
from prometheus_core.execution.durable_state import save_state, load_state
from prometheus_core.mcp.host import app as mcp_app

app = FastAPI(title="PROMETHEUS Daemon")

planner = PlannerAgent()
coder = CoderAgent()
executor = ExecutorAgent()
reflection = ReflectionAgent()

state = load_state()

@app.get("/")
def root():
    return {"message": "PROMETHEUS Daemon is running"}

@app.post("/chat")
def chat(message: str = Query(...)):
    plan = planner.run(message)
    code = coder.run(plan)
    result = executor.run(code)
    reflection.run(result)
    
    state["last_message"] = message
    state["last_result"] = result
    save_state(state)
    
    return {"response": result}

# Mount MCP
app.mount("/mcp", mcp_app)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
