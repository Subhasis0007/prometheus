import os
import subprocess
import re

def clean_code(raw_code):
    code = raw_code.strip()
    
    # Remove markdown
    if "```python" in code:
        code = code.split("```python", 1)[1]
    if "```" in code:
        code = code.split("```", 1)[0]
    
    # Remove junk
    for junk in ["Assistant:", "Human:", "No comments.", "No extra spaces"]:
        code = code.replace(junk, "")
    
    # Keep only from first import/def
    lines = code.split("\n")
    for i, line in enumerate(lines):
        if line.strip().startswith(("import ", "from ", "def ")):
            code = "\n".join(lines[i:])
            break
    
    return code.strip()

def executor_agent(code, tools_dir):
    # Clean the code first
    clean = clean_code(code)
    
    filename = f"tool_{len(os.listdir(tools_dir)) + 1}.py"
    filepath = os.path.join(tools_dir, filename)
    
    with open(filepath, "w") as f:
        f.write(clean)
    
    try:
        result = subprocess.run(
            ["python", filepath],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return f"✅ Tool {filename} executed successfully!\n{result.stdout}"
        else:
            return f"❌ Error in {filename}:\n{result.stderr}"
    except Exception as e:
        return f"❌ Sandbox Error: {str(e)}"