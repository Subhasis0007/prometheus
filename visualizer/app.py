from flask import Flask, render_template, redirect, url_for
import os
import glob
import re
import subprocess

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
REPORTS_DIR = os.path.join(PROJECT_ROOT, "artifacts", "run_reports")

def get_run_reports():
    if not os.path.exists(REPORTS_DIR):
        return []
    reports = sorted(glob.glob(os.path.join(REPORTS_DIR, "run_*.md")), reverse=True)
    runs = []
    for path in reports:
        filename = os.path.basename(path)
        with open(path, "r") as f:
            content = f.read()
        
        steps = re.search(r'(\d+)/(\d+)', content)
        steps_display = f"{steps.group(1)}/{steps.group(2)}" if steps else "N/A"
        
        ts = re.search(r'\*\*Timestamp:\*\* (.+)', content)
        goal = re.search(r'\*\*Goal:\*\* (.+)', content)
        status = re.search(r'\*\*Status:\*\* (.+)', content)
        code = re.search(r'```python\n(.*?)```', content, re.DOTALL)
        
        runs.append({
            "filename": filename,
            "timestamp": ts.group(1) if ts else "Unknown",
            "goal": goal.group(1)[:65] + "..." if goal else "N/A",
            "status": status.group(1) if status else "Unknown",
            "steps": steps_display,
            "content": content,
            "code_block": code.group(1).strip() if code else ""
        })
    return runs

@app.route("/")
def index():
    runs = get_run_reports()
    return render_template("index.html", runs=runs)

@app.route("/run/<filename>")
def view_run(filename):
    path = os.path.join(REPORTS_DIR, filename)
    with open(path, "r") as f:
        content = f.read()
    code = re.search(r'```python\n(.*?)```', content, re.DOTALL)
    return render_template("run.html", filename=filename, content=content, code_block=code.group(1).strip() if code else "")

@app.route("/rerun/<filename>")
def rerun(filename):
    path = os.path.join(REPORTS_DIR, filename)
    if not os.path.exists(path):
        return "Report not found", 404
    
    with open(path, "r") as f:
        content = f.read()
    
    goal_match = re.search(r'\*\*Goal:\*\* (.+?)(?:\n|$)', content)
    if not goal_match:
        return "Could not extract goal", 400
    
    goal = goal_match.group(1).strip()
    print(f"\n[Visualizer] Re-running goal from UI: {goal[:80]}...")
    
    try:
        result = subprocess.run(
            ["uv", "run", "python", "main.py", "rerun", "1"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=300
        )
        print(result.stdout[-2000:] if len(result.stdout) > 2000 else result.stdout)
    except Exception as e:
        print(f"Rerun error: {e}")
    
    return redirect(url_for('index'))

@app.route("/delete/<filename>")
def delete_run(filename):
    path = os.path.join(REPORTS_DIR, filename)
    if os.path.exists(path):
        os.remove(path)
        print(f"[Visualizer] Deleted run: {filename}")
    return redirect(url_for('index'))

if __name__ == "__main__":
    print("🚀 Starting Prometheus Visualizer...")
    app.run(debug=True, port=5000)
