import os

# 1. Create the dedicated UI file
html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PROMETHEUS | Team Collaboration</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background-color: #0d1117; color: #c9d1d9; margin: 0; padding: 20px; }
        .container { max-width: 900px; margin: 0 auto; }
        h1 { color: #58a6ff; font-weight: 600; border-bottom: 1px solid #30363d; padding-bottom: 10px; }
        .input-group { display: flex; gap: 10px; margin-bottom: 20px; }
        input[type="text"] { flex-grow: 1; padding: 12px; border-radius: 6px; border: 1px solid #30363d; background-color: #161b22; color: #c9d1d9; font-size: 16px; }
        button { padding: 12px 24px; background-color: #238636; color: white; border: none; border-radius: 6px; font-weight: 600; cursor: pointer; transition: 0.2s; }
        button:hover { background-color: #2ea043; }
        button:disabled { background-color: #21262d; color: #8b949e; cursor: not-allowed; }
        .chat-box { background-color: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 20px; min-height: 400px; display: flex; flex-direction: column; gap: 15px; }
        .message { padding: 15px; border-radius: 6px; background-color: #0d1117; border-left: 4px solid #30363d; }
        .agent-researcher { border-left-color: #3b82f6; }
        .agent-coder { border-left-color: #10b981; }
        .agent-reviewer { border-left-color: #ef4444; }
        .agent-prometheus { border-left-color: #8b5cf6; }
        .agent-name { font-weight: bold; margin-bottom: 8px; font-size: 0.9em; text-transform: uppercase; letter-spacing: 1px; }
        pre { background: #000; padding: 10px; border-radius: 4px; overflow-x: auto; white-space: pre-wrap; font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace; font-size: 14px; }
        .loading { display: none; color: #8b949e; font-style: italic; margin-bottom: 15px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>PROMETHEUS Team Protocol</h1>
        <div class="input-group">
            <input type="text" id="task-input" placeholder="Enter task for the agent team (e.g., 'Write a python script to parse a CSV and output JSON')" onkeypress="if(event.key === 'Enter') runTeam()">
            <button id="run-btn" onclick="runTeam()">Execute Workflow</button>
        </div>
        <div class="chat-box" id="chat-box">
            <div style="color: #8b949e; text-align: center; margin-top: 150px;">System Ready. Awaiting task input.</div>
        </div>
        <div class="loading" id="loading-indicator">PROMETHEUS is orchestrating the team... This may take a minute depending on the MLX workload.</div>
    </div>

    <script>
        async function runTeam() {
            const input = document.getElementById('task-input');
            const btn = document.getElementById('run-btn');
            const chatBox = document.getElementById('chat-box');
            const loading = document.getElementById('loading-indicator');
            const task = input.value.trim();

            if (!task) return;

            // UI State update
            input.disabled = true;
            btn.disabled = true;
            chatBox.innerHTML = '';
            loading.style.display = 'block';

            try {
                const response = await fetch('/run/team', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ task: task })
                });

                const result = await response.json();
                loading.style.display = 'none';

                if (result.status === 'success') {
                    result.transcript.forEach(turn => {
                        const div = document.createElement('div');
                        div.className = `message agent-${turn.agent.toLowerCase()}`;
                        div.innerHTML = `<div class="agent-name" style="color: ${getColor(turn.agent)}">${turn.agent}</div><pre>${escapeHtml(turn.content)}</pre>`;
                        chatBox.appendChild(div);
                    });
                } else {
                    chatBox.innerHTML = `<div class="message" style="border-left-color: red; color: red;">Error: ${result.error}</div>`;
                }
            } catch (err) {
                loading.style.display = 'none';
                chatBox.innerHTML = `<div class="message" style="border-left-color: red; color: red;">Network Error: ${err.message}</div>`;
            }

            input.disabled = false;
            btn.disabled = false;
            input.focus();
        }

        function getColor(agent) {
            if (agent === 'Researcher') return '#3b82f6';
            if (agent === 'Coder') return '#10b981';
            if (agent === 'Reviewer') return '#ef4444';
            if (agent === 'PROMETHEUS') return '#8b5cf6';
            return '#c9d1d9';
        }

        function escapeHtml(unsafe) {
            return unsafe
                 .replace(/&/g, "&amp;")
                 .replace(/</g, "&lt;")
                 .replace(/>/g, "&gt;")
                 .replace(/"/g, "&quot;")
                 .replace(/'/g, "&#039;");
        }
    </script>
</body>
</html>"""

os.makedirs('forge/templates', exist_ok=True)
with open('forge/templates/team.html', 'w') as f:
    f.write(html_content)
print("✅ Created forge/templates/team.html")

# 2. Patch forge.py to serve the new HTML page safely
forge_path = 'forge/forge.py'
with open(forge_path, 'r') as f:
    content = f.read()

serve_route = """
@app.get("/team")
async def team_ui(request: Request):
    return templates.TemplateResponse("team.html", {"request": request})
"""

if "@app.get(\"/team\")" not in content:
    if "if __name__ ==" in content:
        content = content.replace("if __name__ ==", serve_route + "\n\nif __name__ ==")
    else:
        content += "\n" + serve_route
    
    with open(forge_path, 'w') as f:
        f.write(content)
    print("✅ Injected /team GET route into forge.py")
else:
    print("⚠️ /team route already exists.")

print("🚀 UI setup complete.")
