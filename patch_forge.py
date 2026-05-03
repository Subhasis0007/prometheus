import os

file_path = 'forge/forge.py'
if not os.path.exists(file_path):
    print(f"Error: {file_path} not found. Are you in the right directory?")
    exit(1)

with open(file_path, 'r') as f:
    lines = f.readlines()

# 1. Add import safely
if not any("PrometheusSupervisor" in line for line in lines):
    # Insert right after the first line to avoid messing up other imports
    lines.insert(1, "from forge.collaboration.team import PrometheusSupervisor\n")

# 2. Add endpoint safely
endpoint_code = """
@app.post("/run/team")
async def run_team_workflow(request: Request):
    data = await request.json()
    task = data.get("task", "")
    if not task:
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=400, content={"error": "Task required"})
        
    try:
        # NOTE: We need to bind this to your actual MLX function. 
        # For now, it points to 'generate_text' (update if yours is named differently)
        def local_mlx_call(prompt):
            # Pass to your local Qwen2.5-7B
            return generate_text(prompt) 

        supervisor = PrometheusSupervisor(mlx_generate_fn=local_mlx_call)
        transcript = supervisor.run_team_task(task)
        
        from fastapi.responses import JSONResponse
        return JSONResponse(content={"status": "success", "task": task, "transcript": transcript})
    except Exception as e:
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"error": str(e)})
"""

content = "".join(lines)
if "@app.post(\"/run/team\")" not in content:
    # Inject right before the standard uvicorn run block
    if "if __name__ ==" in content:
        content = content.replace("if __name__ ==", endpoint_code + "\n\nif __name__ ==")
    else:
        content += "\n" + endpoint_code

    with open(file_path, 'w') as f:
        f.write(content)
    print("✅ PROMETHEUS /run/team endpoint injected into forge/forge.py!")
else:
    print("⚠️ Endpoint already exists, skipping injection.")
