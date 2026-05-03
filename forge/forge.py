"""
Forge - The Unified AI Agent Platform
PROMETHEUS Final Version
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import os

# --- PROMETHEUS MLX ENGINE ---
try:
    from mlx_lm import load, generate
    import logging
    logger = logging.getLogger("PROMETHEUS-MLX")
    logger.info("Initializing Qwen2.5-7B MLX model into memory... This may take a moment.")
    
    # Load globally to persist across API calls
    model, tokenizer = load("mlx-community/Qwen2.5-7B-Instruct-4bit")
    logger.info("✅ MLX Engine Online.")

    def generate_text(prompt: str, max_tokens=2048) -> str:
        # Wrap the MLX generate call
        response = generate(model, tokenizer, prompt=prompt, max_tokens=max_tokens)
        return response
except ImportError:
    print("⚠️ mlx_lm not found. Run: pip install mlx-lm")
    def generate_text(prompt: str, max_tokens=2048) -> str:
        return "Error: mlx-lm not installed."
# -----------------------------

from forge.supervision.log import log_supervision
from forge.memory.skill_display import get_recent_skills
from forge.memory.persistent import save_memory, get_memory
from forge.collaboration.team import PrometheusSupervisor

app = FastAPI(title="Forge - AI Agent Platform")
templates = Jinja2Templates(directory="forge/templates")

@app.get("/")
def root():
    return {"message": "Forge is running", "supervisor": "PROMETHEUS"}

@app.get("/demo", response_class=HTMLResponse)
def demo():
    with open("forge/templates/demo.html") as f:
        return f.read()

@app.get("/chat", response_class=HTMLResponse)
def chat_page():
    with open("forge/templates/chat.html") as f:
        return f.read()

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    with open("forge/templates/dashboard.html") as f:
        return f.read()

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    message = data.get("message", "")
    response = f"PROMETHEUS: I received '{message}'. Memory: {get_memory('last_request')}"
    save_memory("last_request", message)
    log_supervision("Chat", message, response)
    return {"response": response}

@app.get("/skills")
def get_skills():
    return {"recent_skills": get_recent_skills(5)}

@app.get("/memory")
def get_last_memory():
    return {"last_request": get_memory('last_request')}

@app.get("/git")
def git_status():
    return {"git": "Git branch: main (active)"}

@app.post("/run/team")
async def run_team_workflow(request: Request):
    data = await request.json()
    task = data.get("task", "")
    if not task:
        return JSONResponse(status_code=400, content={"error": "Task required"})
        
    try:
        def local_mlx_call(prompt):
            # Pass to your local Qwen2.5-7B
            return generate_text(prompt) 

        supervisor = PrometheusSupervisor(mlx_generate_fn=local_mlx_call)
        transcript = supervisor.run_team_task(task)
        
        return JSONResponse(content={"status": "success", "task": task, "transcript": transcript})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/team")
async def team_ui(request: Request):
    return templates.TemplateResponse("team.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8002)
