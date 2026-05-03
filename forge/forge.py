"""
Forge - The Unified AI Agent Platform
PROMETHEUS Dashboard
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import uvicorn
from forge.supervision.log import log_supervision
from forge.memory.skill_display import get_recent_skills
from forge.memory.persistent import save_memory, get_memory
from forge.collaboration.team import collaborate_on_task

forge_app = FastAPI(title="Forge - AI Agent Platform")

@forge_app.get("/")
def root():
    return {"message": "Forge is running", "supervisor": "PROMETHEUS"}

@forge_app.get("/demo", response_class=HTMLResponse)
def demo():
    with open("forge/templates/demo.html") as f:
        return f.read()

@forge_app.get("/chat", response_class=HTMLResponse)
def chat_page():
    with open("forge/templates/chat.html") as f:
        return f.read()

@forge_app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    with open("forge/templates/dashboard.html") as f:
        return f.read()

@forge_app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    message = data.get("message", "")
    response = f"PROMETHEUS: I received '{message}'. Memory: {get_memory('last_request')}"
    save_memory("last_request", message)
    log_supervision("Chat", message, response)
    return {"response": response}

@forge_app.get("/skills")
def get_skills():
    return {"recent_skills": get_recent_skills(5)}

@forge_app.get("/memory")
def get_last_memory():
    return {"last_request": get_memory('last_request')}

@forge_app.get("/git")
def git_status():
    return {"git": "Git branch: main (active)"}

@forge_app.post("/run/collaborate")
async def run_collaboration(request: Request):
    data = await request.json()
    task = data.get("task", "Build something")
    result = collaborate_on_task(task)
    log_supervision("Collaboration", task, str(result))
    return result

if __name__ == "__main__":
    uvicorn.run(forge_app, host="127.0.0.1", port=8002)
