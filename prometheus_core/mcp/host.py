from fastapi import FastAPI
import uvicorn

app = FastAPI(title="PROMETHEUS MCP Host")

@app.get("/mcp")
def mcp_info():
    return {"protocol": "MCP", "version": "1.0", "capabilities": ["tool_call", "memory_access"]}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
